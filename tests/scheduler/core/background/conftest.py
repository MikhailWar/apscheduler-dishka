import pytest
from apscheduler.schedulers.background import BackgroundScheduler


@pytest.fixture
def background_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    yield scheduler
    scheduler.shutdown()
