from collections.abc import Container

import pytest
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler

from apscheduler_dishka import inject, setup_dishka
from tests.common import run_sync_job


@pytest.mark.parametrize(
    "scheduler",
    [
        BackgroundScheduler(),
    ],
    ids=[
        "background",
    ],
)
def test_scheduler_sync_inject(
        scheduler: BaseScheduler,
        container_dishka: Container,
):
    command_data = "test_scheduler_sync_inject"

    setup_dishka(
        container=container_dishka,
        scheduler=scheduler,
        auto_inject=False,
    )

    scheduler.start()

    result = run_sync_job(
        scheduler=scheduler,
        command_data=command_data,
        inject_func=inject,
    )

    assert command_data == result


@pytest.mark.parametrize(
    "scheduler",
    [
        BackgroundScheduler(),
    ],
    ids=[
        "blocking",
    ],
)
def test_scheduler_auto_sync_inject(
        scheduler: BaseScheduler,
        container_dishka: Container,
):
    command_data = "test_scheduler_auto_sync_inject"

    setup_dishka(
        container=container_dishka,
        scheduler=scheduler,
        auto_inject=True,
    )

    scheduler.start()

    result = run_sync_job(
        scheduler=scheduler,
        command_data=command_data,
    )

    assert command_data == result
