from unittest.mock import Mock

import pytest
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import AsyncContainer, Container

from apscheduler_dishka import (
    AsyncDishkaSchedulerExecutor,
    DishkaSchedulerExecutor,
)
from apscheduler_dishka.errors import FailedToSetupDishkaContainerError
from apscheduler_dishka.integration import create_executor


def test_create_async_executor():
    scheduler = Mock(spec=AsyncIOScheduler)
    scheduler._create_default_executor.return_value = AsyncIOExecutor()  # noqa: SLF001

    container = Mock(spec=AsyncContainer)
    inject_func = Mock()

    executor = create_executor(
        scheduler=scheduler,
        dishka_container=container,
        inject_func=inject_func,
    )

    assert isinstance(executor, AsyncDishkaSchedulerExecutor)


def test_create_sync_executor():
    scheduler = Mock()
    scheduler._create_default_executor.return_value = ThreadPoolExecutor()  # noqa: SLF001

    container = Mock(spec=Container)
    inject_func = Mock()

    executor = create_executor(
        scheduler=scheduler,
        dishka_container=container,
        inject_func=inject_func,
    )

    assert isinstance(executor, DishkaSchedulerExecutor)


def test_error_async_executor_with_sync_container():
    scheduler = Mock()
    scheduler._create_default_executor.return_value = AsyncIOExecutor()  # noqa: SLF001

    container = Mock(spec=Container)
    inject_func = Mock()

    with pytest.raises(FailedToSetupDishkaContainerError):
        create_executor(
            scheduler=scheduler,
            dishka_container=container,
            inject_func=inject_func,
        )


def test_error_async_container_with_sync_scheduler():
    scheduler = Mock()
    scheduler._create_default_executor.return_value = ThreadPoolExecutor()  # noqa: SLF001

    container = Mock(spec=AsyncContainer)
    inject_func = Mock()

    with pytest.raises(FailedToSetupDishkaContainerError):
        create_executor(
            scheduler=scheduler,
            dishka_container=container,
            inject_func=inject_func,
        )
