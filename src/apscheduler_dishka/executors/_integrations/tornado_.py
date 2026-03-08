from abc import ABC

from apscheduler.executors.base import BaseExecutor

try:
    from apscheduler.executors.tornado import TornadoExecutor
except ImportError:
    class TornadoExecutor(BaseExecutor, ABC):  # type: ignore[misc, no-redef]
        ...

__all__ = (
    "TornadoExecutor",
)
