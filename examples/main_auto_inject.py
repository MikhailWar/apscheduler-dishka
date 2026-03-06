import logging
from abc import abstractmethod
from typing import Protocol

from apscheduler.schedulers.blocking import BlockingScheduler
from dishka import FromDishka, Provider, Scope, make_container, provide

from apscheduler_dishka.integration import setup_dishka


class IRepository(Protocol):
    @abstractmethod
    def get(self, data: str) -> str:
        raise NotImplementedError


class ImplRepository(IRepository):
    def get(self, data: str) -> str:
        return f"Hello, i am repository. This is {data}"


class Interactor:
    def __init__(self, repo: IRepository) -> None:
        self._repo = repo

    def __call__(self, data: str) -> str:
        return self._repo.get(data)


class AdaptersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def repository(self) -> IRepository:
        return ImplRepository()


class InteractorProvider(Provider):
    interactor = provide(Interactor, scope=Scope.REQUEST)


def task_1(
        data: str,
        interactor: FromDishka[Interactor],
):
    interactor(data)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    scheduler = BlockingScheduler()
    container = make_container(AdaptersProvider(), InteractorProvider())
    setup_dishka(
        container=container,
        scheduler=scheduler,
        auto_inject=True,
    )

    scheduler.add_job(
        task_1,
        trigger="interval",
        seconds=5,
        args=["World"],
    )
    scheduler.add_job(
        task_1,
        trigger="interval",
        seconds=5,
        kwargs={"data": "Hello"},
    )

    try:
        scheduler.start()
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
