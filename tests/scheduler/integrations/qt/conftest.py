import pytest
from apscheduler.schedulers.qt import QtScheduler


@pytest.fixture
def qt_scheduler():
    scheduler = QtScheduler()
    scheduler.start()
    yield scheduler
    scheduler.shutdown()
