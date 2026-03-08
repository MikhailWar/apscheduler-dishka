import threading

from apscheduler.schedulers.twisted import TwistedScheduler
from dishka import Container

from apscheduler_dishka import inject, setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    WAIT_TIMEOUT_EVENT_SECONDS,
    tracked_execute_task,
)


def test_twisted_scheduler_inject(
        twisted_scheduler: TwistedScheduler,
        container_dishka: Container,
        twisted_reactor,
):
    event_done = threading.Event()

    setup_dishka(
        container=container_dishka,
        scheduler=twisted_scheduler,
    )

    tracked_execute_task(
        scheduler=twisted_scheduler,
        event_done=event_done,
        inject_func=inject,
    )

    twisted_reactor.callFromThread(twisted_scheduler.start)

    assert event_done.wait(
        timeout=WAIT_TIMEOUT_EVENT_SECONDS,
    ), NOT_RUNNING_JOB_ERROR


def test_twisted_scheduler_auto_inject(
        twisted_scheduler: TwistedScheduler,
        container_dishka: Container,
        twisted_reactor,
):
    event_done = threading.Event()

    setup_dishka(
        container=container_dishka,
        scheduler=twisted_scheduler,
        auto_inject=True,
    )

    tracked_execute_task(
        scheduler=twisted_scheduler,
        event_done=event_done,
    )

    twisted_reactor.callFromThread(twisted_scheduler.start)

    assert event_done.wait(
        timeout=WAIT_TIMEOUT_EVENT_SECONDS,
    ), NOT_RUNNING_JOB_ERROR
