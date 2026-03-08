import time
from abc import ABC, abstractmethod
from asyncio import Protocol
from typing import Final, ParamSpec, TypeVar

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from dishka import FromDishka, Provider, Scope, provide
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

    async def get_async(self, data: str) -> str:
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


P = ParamSpec("P")
T = TypeVar("T")

NOT_RUNNING_JOB_ERROR: Final[str] = "Job is not running"
WAIT_TIMEOUT_EVENT_SECONDS: int = 2


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

    scheduler.add_job(
        job,
        trigger="date",
        kwargs={"_command_data": command_data},
    )
    time.sleep(1)
    return result


class Event(Protocol):
    def set(self): ...

    def is_set(self) -> bool: ...


def tracked_execute_task(
        scheduler: BaseScheduler,
        event_done: Event,
        inject_func: InjectFunc[P, T] = None,
):
    def task(interactor: FromDishka[Interactor]):
        interactor.execute("Running in task event")
        event_done.set()

    if inject_func is not None:
        task = inject_func(task)

    scheduler.add_job(task, "date")


def tracked_execute_async_task(
        scheduler: BaseScheduler,
        event_done: Event,
        inject_func: InjectFunc[P, T] = None,
):
    async def task(interactor: FromDishka[Interactor]):
        await interactor.async_execute("Running in task event")
        event_done.set()

    if inject_func is not None:
        task = inject_func(task)

    scheduler.add_job(task, "date")
