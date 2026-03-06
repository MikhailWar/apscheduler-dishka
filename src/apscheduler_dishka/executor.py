import datetime
from typing import TypeVar, ParamSpec, Container, Final

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from dishka import AsyncContainer
from dishka.integrations.base import is_dishka_injected, InjectFunc

P = ParamSpec("P")
T = TypeVar("T")

DISHKA_CONTAINER_KEY: Final[str] = "dishka_container"


class DishkaSchedulerExecutor(ThreadPoolExecutor):
    def __init__(
            self,
            inject_func: InjectFunc[P, T],
            dishka_container: Container | AsyncContainer

    ):
        super().__init__()
        self._inject_func = inject_func
        self._dishka_container = dishka_container

    def _do_submit_job(self, job: Job, run_times: list[datetime.datetime]):
        if not is_dishka_injected(job.func):
            job.func = self._inject_func(job.func)
        job.kwargs[DISHKA_CONTAINER_KEY] = self._dishka_container
        return super()._do_submit_job(
            job=job,
            run_times=run_times
        )


class AsyncDishkaSchedulerExecutor(AsyncIOExecutor):
    def __init__(
            self,
            inject_func: InjectFunc[P, T],
            dishka_container: Container | AsyncContainer

    ):
        super().__init__()
        self._inject_func = inject_func
        self._dishka_container = dishka_container


    def _do_submit_job(self, job: Job, run_times: list[datetime.datetime]):
        if not is_dishka_injected(job.func):
            job.func = self._inject_func(job.func)
        job.kwargs[DISHKA_CONTAINER_KEY] = self._dishka_container
        return super()._do_submit_job(
            job=job,
            run_times=run_times
        )
