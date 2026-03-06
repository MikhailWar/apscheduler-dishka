import pytest
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from dishka import (
    AsyncContainer,
    Container,
    make_async_container,
    make_container,
)

from apscheduler_dishka import setup_dishka
from tests.common import AppProvider


class SchedulerAutoInject(BackgroundScheduler):
    ...


@pytest.fixture
def container_dishka() -> Container:
    return make_container(
        AppProvider(),
    )


@pytest.fixture
def async_container_dishka() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
    )


@pytest.fixture
def sync_scheduler(
        container_dishka: Container,
) -> BlockingScheduler:
    scheduler = BackgroundScheduler()
    setup_dishka(
        container=container_dishka,
        scheduler=scheduler,
        auto_inject=False,
    )
    scheduler.start()
    yield scheduler
    scheduler.shutdown()


@pytest.fixture
def sync_scheduler_auto_inject(
        container_dishka: Container,
) -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    setup_dishka(
        container=container_dishka,
        scheduler=scheduler,
        auto_inject=True,
    )
    scheduler.start()
    yield scheduler
    scheduler.shutdown()


@pytest.fixture
def jobs_stores_redis_default() -> dict[str, RedisJobStore]:
    job_stores: dict[str, RedisJobStore] = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs",
            run_times_key="dispatched_trips_running",
        ),
    }
    return job_stores


@pytest.fixture
def sync_scheduler_redis_jobstore_inject(
        container_dishka: Container,
        jobs_stores_redis_default: dict[str, RedisJobStore],
) -> BackgroundScheduler:
    scheduler = BackgroundScheduler(
        job_stores=jobs_stores_redis_default,
    )
    setup_dishka(
        container=container_dishka,
        scheduler=scheduler,
        auto_inject=False,
    )
    scheduler.start()
    yield scheduler
    scheduler.shutdown()


@pytest.fixture
def sync_scheduler_redis_jobstore_auto_inject(
        container_dishka: Container,
        jobs_stores_redis_default: dict[str, RedisJobStore],
) -> BackgroundScheduler:
    scheduler = BackgroundScheduler(
        job_stores=jobs_stores_redis_default,
    )
    setup_dishka(
        container=container_dishka,
        scheduler=scheduler,
        auto_inject=True,
    )
    scheduler.start()
    yield scheduler
    scheduler.shutdown()
