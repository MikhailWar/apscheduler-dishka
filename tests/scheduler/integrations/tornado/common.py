from tornado.ioloop import IOLoop, PeriodicCallback

from tests.common import WAIT_TIMEOUT_EVENT_SECONDS, Event


def start_tornado_io_loop_by_event(
        tornado_io_loop: IOLoop,
        event_done: Event,
):
    def check_done():
        if event_done.is_set():
            tornado_io_loop.stop()

    checker = PeriodicCallback(check_done, 100)
    checker.start()

    tornado_io_loop.call_later(
        WAIT_TIMEOUT_EVENT_SECONDS,
        tornado_io_loop.stop,
    )
    tornado_io_loop.start()
