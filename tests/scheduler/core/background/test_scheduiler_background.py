import threading

from apscheduler.schedulers.background import BackgroundScheduler
from dishka import Container

from apscheduler_dishka import inject, setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    WAIT_TIMEOUT_EVENT_SECONDS,
    tracked_execute_task,
)


def test_background_scheduler_inject(
        background_scheduler: BackgroundScheduler,
        container_dishka: Container,
):
    setup_dishka(
        container=container_dishka,
        scheduler=background_scheduler,
        auto_inject=False,
    )

    event_done = threading.Event()
    tracked_execute_task(
        scheduler=background_scheduler,
        event_done=event_done,
        inject_func=inject,
    )

    event_done.wait(timeout=WAIT_TIMEOUT_EVENT_SECONDS), NOT_RUNNING_JOB_ERROR


def test_background_scheduler_auto_inject(
        background_scheduler: BackgroundScheduler,
        container_dishka: Container,
):
    setup_dishka(
        container=container_dishka,
        scheduler=background_scheduler,
        auto_inject=True,
    )

    event_done = threading.Event()
    tracked_execute_task(
        scheduler=background_scheduler,
        event_done=event_done,
    )

    event_done.wait(timeout=WAIT_TIMEOUT_EVENT_SECONDS), NOT_RUNNING_JOB_ERROR
