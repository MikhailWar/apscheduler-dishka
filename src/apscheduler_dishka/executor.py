import datetime
from typing import TypeVar, ParamSpec

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from dishka.integrations.base import is_dishka_injected, InjectFunc

P = ParamSpec("P")
T = TypeVar("T")


class DishkaSchedulerExecutor(ThreadPoolExecutor):

    def __init__(self, inject_func: InjectFunc[P, T]):
        super().__init__()
        self._inject_func = inject_func

    def _do_submit_job(self, job: Job, run_times: list[datetime.datetime]):
        if not is_dishka_injected(job.func):
            job.func = self._inject_func(job.func)
        return super()._do_submit_job(
            job, run_times
        )
