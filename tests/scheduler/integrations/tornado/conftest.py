import pytest
from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.ioloop import IOLoop


@pytest.fixture
def tornado_scheduler():
    scheduler = TornadoScheduler()
    scheduler.start()
    yield scheduler
    scheduler.shutdown()


@pytest.fixture(scope="session")
def tornado_io_loop():
    loop = IOLoop.current()
    yield loop
    loop.close()
