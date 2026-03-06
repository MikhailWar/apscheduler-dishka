from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler_dishka import inject
from tests.common import run_sync_job


def test_apscheduler_inject_sync(
        sync_scheduler: BackgroundScheduler,
):
    command_data = "test_apscheduler_inject_sync"
    assert command_data == run_sync_job(
        scheduler=sync_scheduler,
        command_data=command_data,
        inject_func=inject,
    )


def test_apscheduler_auto_inject_sync(
        sync_scheduler_auto_inject: BackgroundScheduler,
):
    command_data = "test_apscheduler_inject_sync"
    assert command_data == run_sync_job(
        scheduler=sync_scheduler_auto_inject,
        command_data=command_data,
    )
