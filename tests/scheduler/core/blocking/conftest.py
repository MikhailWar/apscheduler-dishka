import threading

import pytest
from apscheduler.schedulers.blocking import BlockingScheduler


@pytest.fixture
def blocking_scheduler():
    scheduler = BlockingScheduler()

    thread = threading.Thread(target=scheduler.start)
    thread.start()

    yield scheduler

    scheduler.shutdown()
    thread.join()
