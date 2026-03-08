from unittest.mock import Mock

import pytest
from apscheduler.executors.base import BaseExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from dishka import AsyncContainer, Container
from dishka.integrations.base import is_dishka_injected

from apscheduler_dishka import inject, inject_executor
from apscheduler_dishka.errors import FailedToInjectDishkaContainerError
from apscheduler_dishka.executors.inject import DISHKA_CONTAINER_KEY


@pytest.mark.parametrize(
    "executor",
    [
        ThreadPoolExecutor(),

    ],
    ids=[
        "thread_executor",
    ],
)
def test_error_inject_executor(
        executor: BaseExecutor,
        async_container_dishka: AsyncContainer,
):
    with pytest.raises(FailedToInjectDishkaContainerError):
        inject_executor(
            executor=executor,
            dishka_container=async_container_dishka,
            inject_func=inject,
        )


def test_inject_executor(
        container_dishka: Container,
):
    executor = Mock(spec=ThreadPoolExecutor)
    original_do_submit_job = executor._do_submit_job  # noqa: SLF001
    inject_executor(
        executor=executor,
        dishka_container=container_dishka,
        inject_func=inject,
    )

    def test_job(): ...

    job = Mock(spec=Job)
    job.func = test_job
    job.kwargs = {}
    executor._do_submit_job(job, run_times=[])  # noqa: SLF001

    assert is_dishka_injected(job.func) is True
    assert executor._do_submit_job != original_do_submit_job  # noqa: SLF001
    assert job.kwargs[DISHKA_CONTAINER_KEY] == container_dishka
