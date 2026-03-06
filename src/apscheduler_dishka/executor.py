import datetime
from typing import Final, ParamSpec, TypeVar

from apscheduler.executors.asyncio import (
    AsyncIOExecutor,
)
from apscheduler.executors.pool import (
    ThreadPoolExecutor,
)
from apscheduler.job import Job
from dishka import AsyncContainer, Container
from dishka.integrations.base import InjectFunc, is_dishka_injected

P = ParamSpec("P")
T = TypeVar("T")

DISHKA_CONTAINER_KEY: Final[str] = "dishka_container"


class DishkaSchedulerExecutor(ThreadPoolExecutor):  # type: ignore[misc]
    def __init__(
            self,
            inject_func: InjectFunc[P, T],
            dishka_container: Container,

    ):
        super().__init__()
        self._inject_func = inject_func
        self._dishka_container = dishka_container

    def _do_submit_job(
            self,
            job: Job,
            run_times: list[datetime.datetime],
    ) -> None:
        if not is_dishka_injected(job.func):
            job.func = self._inject_func(job.func)
        job.kwargs[DISHKA_CONTAINER_KEY] = self._dishka_container
        super()._do_submit_job(
            job=job,
            run_times=run_times,
        )


class AsyncDishkaSchedulerExecutor(AsyncIOExecutor):  # type: ignore[misc]
    def __init__(
            self,
            inject_func: InjectFunc[P, T],
            dishka_container: AsyncContainer,

    ):
        super().__init__()
        self._inject_func = inject_func
        self._dishka_container = dishka_container

    def _do_submit_job(
            self,
            job: Job,
            run_times: list[datetime.datetime],
    ) -> None:
        if not is_dishka_injected(job.func):
            job.func = self._inject_func(job.func)
        job.kwargs[DISHKA_CONTAINER_KEY] = self._dishka_container
        super()._do_submit_job(
            job=job,
            run_times=run_times,
        )
