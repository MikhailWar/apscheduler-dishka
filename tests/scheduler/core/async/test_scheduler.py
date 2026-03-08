import asyncio
from contextlib import asynccontextmanager

import pytest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer
from dishka.integrations.base import InjectFunc

from apscheduler_dishka import setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    WAIT_TIMEOUT_EVENT_SECONDS,
    P,
    T,
    tracked_execute_async_task,
)


@asynccontextmanager
async def create_async_scheduler(
        container: AsyncContainer,
        *,
        auto_inject: bool | InjectFunc[P, T] = False,
) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    setup_dishka(
        container=container,
        scheduler=scheduler,
        auto_inject=auto_inject,
    )
    scheduler.start()
    yield scheduler
    scheduler.shutdown()


@pytest.mark.asyncio
async def test_apscheduler_async_inject(
        async_container_dishka: AsyncContainer,
):
    event_done = asyncio.Event()
    async with create_async_scheduler(
            container=async_container_dishka,
            auto_inject=True,
    ) as scheduler:
        tracked_execute_async_task(
            scheduler=scheduler,
            event_done=event_done,
        )

        assert await asyncio.wait_for(
            event_done.wait(),
            timeout=WAIT_TIMEOUT_EVENT_SECONDS,
        ), NOT_RUNNING_JOB_ERROR


@pytest.mark.asyncio
async def test_apscheduler_async_auto_inject(
        async_container_dishka: AsyncContainer,
):
    event_done = asyncio.Event()
    async with create_async_scheduler(
            container=async_container_dishka,
            auto_inject=True,
    ) as scheduler:
        tracked_execute_async_task(
            scheduler=scheduler,
            event_done=event_done,
        )

        assert await asyncio.wait_for(
            event_done.wait(),
            timeout=WAIT_TIMEOUT_EVENT_SECONDS,
        ), NOT_RUNNING_JOB_ERROR
