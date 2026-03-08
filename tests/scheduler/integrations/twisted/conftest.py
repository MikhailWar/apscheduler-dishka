import threading

import pytest
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor


@pytest.fixture
def twisted_scheduler() -> TwistedScheduler:
    return TwistedScheduler()


@pytest.fixture(scope="module")
def twisted_reactor():
    reactor_thread = threading.Thread(
        target=reactor.run,
        kwargs={
            "installSignalHandlers": False,
        },
    )
    reactor_thread.daemon = True
    reactor_thread.start()
    yield reactor
    reactor.callFromThread(reactor.stop)
    reactor_thread.join()
