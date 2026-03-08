import threading

from apscheduler.jobstores.redis import RedisJobStore
from dishka import Container

from apscheduler_dishka import inject, setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    WAIT_TIMEOUT_EVENT_SECONDS,
    tracked_execute_task,
)


def test_apscheduler_redis_jobstore_inject(
        background_scheduler_use_redis_jobstore: dict[str, RedisJobStore],
        container_dishka: Container,
):
    setup_dishka(
        container=container_dishka,
        scheduler=background_scheduler_use_redis_jobstore,
        auto_inject=False,
    )

    event_done = threading.Event()
    tracked_execute_task(
        scheduler=background_scheduler_use_redis_jobstore,
        event_done=event_done,
        inject_func=inject,
    )

    event_done.wait(timeout=WAIT_TIMEOUT_EVENT_SECONDS), NOT_RUNNING_JOB_ERROR


def test_apscheduler_redis_jobstore_auto_inject(
        background_scheduler_use_redis_jobstore: dict[str, RedisJobStore],
        container_dishka: Container,
):
    setup_dishka(
        container=container_dishka,
        scheduler=background_scheduler_use_redis_jobstore,
        auto_inject=True,
    )

    event_done = threading.Event()
    tracked_execute_task(
        scheduler=background_scheduler_use_redis_jobstore,
        event_done=event_done,
        inject_func=inject,
    )

    event_done.wait(timeout=WAIT_TIMEOUT_EVENT_SECONDS), NOT_RUNNING_JOB_ERROR
