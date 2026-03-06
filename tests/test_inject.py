from dishka.integrations.base import is_dishka_injected

from apscheduler_dishka import inject
from tests.common import task


def test_task_inject():
    task_injected = inject(task)

    assert is_dishka_injected(task_injected) is True
    assert task_injected.__name__ == task.__name__
