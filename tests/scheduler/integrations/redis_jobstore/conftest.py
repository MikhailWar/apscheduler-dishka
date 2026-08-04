from collections.abc import Iterator

import pytest
from apscheduler.jobstores.redis import RedisJobStore
from redis.exceptions import RedisError


@pytest.fixture
def jobs_stores_redis_default() -> Iterator[dict[str, RedisJobStore]]:
    job_store = RedisJobStore(
        jobs_key="dispatched_trips_jobs",
        run_times_key="dispatched_trips_running",
    )
    try:
        job_store.redis.ping()
    except RedisError as error:
        pytest.skip(f"Redis is not available: {error}")

    job_store.remove_all_jobs()
    yield {"default": job_store}
    job_store.remove_all_jobs()
