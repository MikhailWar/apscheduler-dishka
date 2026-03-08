from apscheduler.schedulers.gevent import GeventScheduler
from dishka import Container
from gevent.event import Event

from apscheduler_dishka import inject, setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    WAIT_TIMEOUT_EVENT_SECONDS,
    tracked_execute_task,
)


def test_gevent_scheduler_inject(
        gevent_scheduler: GeventScheduler,
        container_dishka: Container,
):
    event_done = Event()
    g = gevent_scheduler.start()
    setup_dishka(
        container=container_dishka,
        scheduler=gevent_scheduler,
        auto_inject=False,
    )

    tracked_execute_task(
        scheduler=gevent_scheduler,
        event_done=event_done,
        inject_func=inject,
    )

    assert event_done.wait(
        timeout=WAIT_TIMEOUT_EVENT_SECONDS,
    ), NOT_RUNNING_JOB_ERROR

    gevent_scheduler.shutdown(wait=False)
    g.kill()


def test_gevent_scheduler_task_auto_inject(
        gevent_scheduler: GeventScheduler,
        container_dishka: Container,
):
    event_done = Event()
    g = gevent_scheduler.start()
    setup_dishka(
        container=container_dishka,
        scheduler=gevent_scheduler,
        auto_inject=True,
    )

    tracked_execute_task(
        scheduler=gevent_scheduler,
        event_done=event_done,
    )

    assert event_done.wait(
        timeout=WAIT_TIMEOUT_EVENT_SECONDS,
    ), NOT_RUNNING_JOB_ERROR

    gevent_scheduler.shutdown(wait=False)
    g.kill()
