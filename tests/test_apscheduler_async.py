import asyncio

import pytest
from dishka import AsyncContainer, FromDishka

from apscheduler_dishka import inject
from tests.common import Interactor, create_async_scheduler


@pytest.mark.asyncio
async def test_apscheduler_async_inject(
        async_container_dishka: AsyncContainer,
):
    async with create_async_scheduler(
            container=async_container_dishka,
            auto_inject=False,
    ) as scheduler:
        result = None

        command_data = "test_apscheduler_async_inject"

        async def job(data: str, interactor: FromDishka[Interactor]):
            nonlocal result
            result = interactor.execute(data)

        scheduler.add_job(inject(job), "date", kwargs={
            "data": command_data,
        })

        await asyncio.sleep(1)
        assert result == command_data


@pytest.mark.asyncio
async def test_apscheduler_async_auto_inject(
        async_container_dishka: AsyncContainer,
):
    async with create_async_scheduler(
            container=async_container_dishka,
            auto_inject=True,
    ) as scheduler:
        result = None

        command_data = "test_apscheduler_auto_inject"

        async def job(data: str, interactor: FromDishka[Interactor]):
            nonlocal result
            result = interactor.execute(data)

        scheduler.add_job(job, "date", kwargs={
            "data": command_data,
        })

        await asyncio.sleep(1)
        assert result == command_data
