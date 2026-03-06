import datetime
import time
from abc import abstractmethod, ABC
from asyncio import Protocol
from typing import ParamSpec, TypeVar

from apscheduler.schedulers.background import BackgroundScheduler
from dishka import provide, Scope, Provider, FromDishka
from dishka.integrations.base import InjectFunc


class IRepository(Protocol, ABC):
    @abstractmethod
    def get(self, data: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_async(self, data: str) -> str:
        raise NotImplementedError


class ImplRepository(IRepository):
    def get(self, data: str) -> str:
        return data

    def get_async(self, data: str) -> str:
        return data


class Interactor:
    def __init__(self, repo: IRepository) -> None:
        self._repo = repo

    def execute(self, data: str) -> str:
        return self._repo.get(data)

    async def async_execute(self, data: str) -> str:
        return await self._repo.get_async(data)


class AppProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    def repository(self) -> IRepository:
        return ImplRepository()

    interactor = provide(Interactor)


def task(
        data: str,
        interactor: FromDishka[Interactor],
):
    result = interactor.execute(data)


P = ParamSpec("P")
T = TypeVar("T")


def run_sync_job(
        scheduler: BackgroundScheduler,
        command_data: str,
        inject_func: InjectFunc[P, T] | None = None,
) -> str:
    result: str = None

    def job(_command_data: str, interactor: FromDishka[Interactor]):
        nonlocal result
        result = interactor.execute(_command_data)

    if inject_func is not None:
        job = inject_func(job)

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=0.5)
    scheduler.add_job(
        job,
        run_date=run_date,
        kwargs={"_command_data": command_data},
    )
    time.sleep(1)

    return result

