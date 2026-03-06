import asyncio
import logging
from abc import abstractmethod
from typing import Protocol

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import FromDishka, Provider, Scope, make_async_container, provide

from apscheduler_dishka.integration import inject, setup_dishka


class IRepository(Protocol):
    @abstractmethod
    async def get(self, data: str) -> str:
        raise NotImplementedError


class ImplRepository(IRepository):
    async def get(self, data: str) -> str:
        return f"Hello, i am repository. This is {data}"


class Interactor:
    def __init__(self, repo: IRepository) -> None:
        self._repo = repo

    async def __call__(self, data: str) -> str:
        return await self._repo.get(data)


class AdaptersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def repository(self) -> IRepository:
        return ImplRepository()


class InteractorProvider(Provider):
    interactor = provide(Interactor, scope=Scope.REQUEST)


@inject
async def async_task_1(
        data: str,
        interactor: FromDishka[Interactor],
):
    await interactor(data)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    scheduler = AsyncIOScheduler()
    container = make_async_container(AdaptersProvider(), InteractorProvider())
    setup_dishka(
        container=container,
        scheduler=scheduler,
        auto_inject=False,
    )

    scheduler.add_job(
        async_task_1,
        trigger="interval",
        seconds=5,
        args=["World"],
    )
    scheduler.add_job(
        async_task_1,
        trigger="interval",
        seconds=5,
        kwargs={"data": "Hello"},
    )

    try:
        scheduler.start()
        while True:
            await asyncio.Event().wait()

    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
