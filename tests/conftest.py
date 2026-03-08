import pytest
from dishka import (
    AsyncContainer,
    Container,
    make_async_container,
    make_container,
)

from tests.common import AppProvider


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
