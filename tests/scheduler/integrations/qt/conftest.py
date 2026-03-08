import pytest
from apscheduler.schedulers.qt import QtScheduler
from PyQt5.QtWidgets import QApplication


@pytest.fixture
def qt_scheduler():
    scheduler = QtScheduler()
    scheduler.start()
    yield scheduler
    scheduler.shutdown()


@pytest.fixture(scope="session")
def q_application():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app
