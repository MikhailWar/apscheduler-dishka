from functools import wraps
from typing import Any, Final, ParamSpec, TypeVar

from apscheduler.executors.asyncio import (
    AsyncIOExecutor,
)
from apscheduler.executors.base import BaseExecutor
from apscheduler.job import Job
from dishka import AsyncContainer, Container
from dishka.integrations.base import InjectFunc, is_dishka_injected

from apscheduler_dishka.errors import FailedToInjectDishkaContainerError

P = ParamSpec("P")
T = TypeVar("T")

DISHKA_CONTAINER_KEY: Final[str] = "dishka_container"


def _inject_job(
        job: Job,
        inject_func: InjectFunc[P, T],
        dishka_container: AsyncContainer | Container,
) -> Job:
    if not is_dishka_injected(job.func):
        job.func = inject_func(job.func)
    job.kwargs[DISHKA_CONTAINER_KEY] = dishka_container

    return job


def inject_executor(
        executor: BaseExecutor,
        dishka_container: AsyncContainer | Container,
        inject_func: InjectFunc[P, T],
) -> BaseExecutor:
    original_do_submit_job = executor._do_submit_job  # noqa: SLF001
    if (
            isinstance(dishka_container, AsyncContainer)
            and not isinstance(executor, AsyncIOExecutor)
    ):
        raise FailedToInjectDishkaContainerError(
            message=f"{executor} not supported AsyncContainer",
        )

    @wraps(executor._do_submit_job)  # noqa: SLF001
    def do_submit_job(
            job: Job,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        job = _inject_job(
            job=job,
            inject_func=inject_func,
            dishka_container=dishka_container,
        )
        return original_do_submit_job(job, *args, **kwargs)

    executor._do_submit_job = do_submit_job  # noqa: SLF001
    return executor
