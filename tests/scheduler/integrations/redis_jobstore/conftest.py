import pytest
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler


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
def background_scheduler_use_redis_jobstore(
        jobs_stores_redis_default: dict[str, RedisJobStore],
):
    scheduler = BackgroundScheduler(
        job_stores=jobs_stores_redis_default,
    )
    scheduler.start()
    yield scheduler
    scheduler.shutdown()
