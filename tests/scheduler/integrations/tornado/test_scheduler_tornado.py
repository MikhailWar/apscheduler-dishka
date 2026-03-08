import asyncio
import threading

from apscheduler.schedulers.tornado import TornadoScheduler
from dishka import Container
from tornado.ioloop import IOLoop

from apscheduler_dishka import inject, setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    tracked_execute_async_task,
    tracked_execute_task,
)
from tests.scheduler.integrations.tornado.common import (
    start_tornado_io_loop_by_event,
)


def test_tornado_scheduler_inject(
        tornado_scheduler: TornadoScheduler,
        container_dishka: Container,
        tornado_io_loop: IOLoop,
):
    event_done = threading.Event()

    setup_dishka(
        container=container_dishka,
        scheduler=tornado_scheduler,
    )

    tracked_execute_task(
        scheduler=tornado_scheduler,
        event_done=event_done,
        inject_func=inject,
    )

    start_tornado_io_loop_by_event(
        tornado_io_loop=tornado_io_loop,
        event_done=event_done,
    )

    assert event_done.is_set()


def test_tornado_scheduler_auto_inject(
        tornado_scheduler: TornadoScheduler,
        container_dishka: Container,
        tornado_io_loop: IOLoop,
):
    event_done = threading.Event()

    setup_dishka(
        container=container_dishka,
        scheduler=tornado_scheduler,
        auto_inject=True,
    )

    tracked_execute_task(
        scheduler=tornado_scheduler,
        event_done=event_done,
    )

    start_tornado_io_loop_by_event(
        tornado_io_loop=tornado_io_loop,
        event_done=event_done,
    )

    assert event_done.is_set()


def test_tornado_scheduler_inject_async(
        tornado_scheduler: TornadoScheduler,
        async_container_dishka: Container,
        tornado_io_loop: IOLoop,
):
    event_done = asyncio.Event()

    setup_dishka(
        container=async_container_dishka,
        scheduler=tornado_scheduler,
        auto_inject=False,
    )

    tracked_execute_async_task(
        scheduler=tornado_scheduler,
        event_done=event_done,
        inject_func=inject,
    )

    start_tornado_io_loop_by_event(
        tornado_io_loop=tornado_io_loop,
        event_done=event_done,
    )

    assert event_done.is_set()


def test_tornado_scheduler_auto_inject_async(
        tornado_scheduler: TornadoScheduler,
        async_container_dishka: Container,
        tornado_io_loop: IOLoop,
):
    event_done = asyncio.Event()

    setup_dishka(
        container=async_container_dishka,
        scheduler=tornado_scheduler,
        auto_inject=True,
    )

    tracked_execute_async_task(
        scheduler=tornado_scheduler,
        event_done=event_done,
    )

    start_tornado_io_loop_by_event(
        tornado_io_loop=tornado_io_loop,
        event_done=event_done,
    )

    assert event_done.is_set(), NOT_RUNNING_JOB_ERROR
