import pytest
from apscheduler.schedulers.gevent import GeventScheduler


@pytest.fixture
def gevent_scheduler():
    return GeventScheduler()
