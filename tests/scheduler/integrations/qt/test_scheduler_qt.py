import threading
import time

from apscheduler.schedulers.qt import QtScheduler
from dishka import Container
from PyQt5.QtWidgets import QApplication

from apscheduler_dishka import inject, setup_dishka
from tests.common import (
    NOT_RUNNING_JOB_ERROR,
    WAIT_TIMEOUT_EVENT_SECONDS,
    tracked_execute_task,
)


def test_qt_scheduler_inject(
        qt_scheduler: QtScheduler,
        container_dishka: Container,
        q_application: QApplication,
):
    event_done = threading.Event()

    setup_dishka(
        container=container_dishka,
        scheduler=qt_scheduler,
    )

    tracked_execute_task(
        scheduler=qt_scheduler,
        event_done=event_done,
        inject_func=inject,
    )

    end_time = time.time() + WAIT_TIMEOUT_EVENT_SECONDS
    while not event_done.is_set() and time.time() < end_time:
        q_application.processEvents()

    assert event_done.is_set(), NOT_RUNNING_JOB_ERROR


def test_qt_scheduler_auto_inject(
        qt_scheduler: QtScheduler,
        container_dishka: Container,
        q_application: QApplication,

):
    event_done = threading.Event()

    setup_dishka(
        container=container_dishka,
        scheduler=qt_scheduler,
        auto_inject=True,
    )

    tracked_execute_task(
        scheduler=qt_scheduler,
        event_done=event_done,
    )

    end_time = time.time() + WAIT_TIMEOUT_EVENT_SECONDS
    while not event_done.is_set() and time.time() < end_time:
        q_application.processEvents()

    assert event_done.is_set(), NOT_RUNNING_JOB_ERROR
