import asyncio
from collections.abc import Callable
from typing import Any, ClassVar

import pytest
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer, FromDishka
from dishka.integrations.base import InjectFunc

from apscheduler_dishka import inject, setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    WAIT_TIMEOUT_EVENT_SECONDS,
    Interactor,
    P,
    T,
)

EXPECTED_RUNS = 2
TASK_DATA = "Running in task event"


class TaskState:
    results: ClassVar[list[str]] = []
    done: ClassVar[asyncio.Event] = asyncio.Event()

    @classmethod
    def reset(cls) -> None:
        cls.results.clear()
        cls.done = asyncio.Event()

    @classmethod
    async def track(cls, interactor: Interactor) -> None:
        cls.results.append(await interactor.async_execute(TASK_DATA))
        if len(cls.results) >= EXPECTED_RUNS:
            cls.done.set()


@inject
async def tracked_task(interactor: FromDishka[Interactor]) -> None:
    await TaskState.track(interactor)


async def auto_injected_task(interactor: FromDishka[Interactor]) -> None:
    await TaskState.track(interactor)


async def run_repeated_task(
        jobstores: dict[str, RedisJobStore],
        container: AsyncContainer,
        func: Callable[..., Any],
        *,
        auto_inject: bool | InjectFunc[P, T] = False,
) -> None:
    TaskState.reset()
    scheduler = AsyncIOScheduler(jobstores=jobstores)
    setup_dishka(
        container=container,
        scheduler=scheduler,
        auto_inject=auto_inject,
    )

    scheduler.add_job(func, trigger="interval", seconds=0.3)
    scheduler.start()

    is_done = True
    try:
        await asyncio.wait_for(
            TaskState.done.wait(),
            timeout=WAIT_TIMEOUT_EVENT_SECONDS,
        )
    except asyncio.TimeoutError:
        is_done = False
    finally:
        scheduler.shutdown(wait=False)

    assert is_done, NOT_RUNNING_JOB_ERROR
    assert TaskState.results[:EXPECTED_RUNS] == [TASK_DATA] * EXPECTED_RUNS


@pytest.mark.asyncio
async def test_apscheduler_redis_jobstore_repeated_run(
        jobs_stores_redis_default: dict[str, RedisJobStore],
        async_container_dishka: AsyncContainer,
):
    await run_repeated_task(
        jobstores=jobs_stores_redis_default,
        container=async_container_dishka,
        func=tracked_task,
        auto_inject=False,
    )


@pytest.mark.asyncio
async def test_apscheduler_redis_jobstore_auto_inject_repeated_run(
        jobs_stores_redis_default: dict[str, RedisJobStore],
        async_container_dishka: AsyncContainer,
):
    await run_repeated_task(
        jobstores=jobs_stores_redis_default,
        container=async_container_dishka,
        func=auto_injected_task,
        auto_inject=True,
    )
