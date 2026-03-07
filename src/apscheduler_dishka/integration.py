from collections.abc import Callable
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, ParamSpec, TypeVar, cast

from apscheduler.job import Job
from apscheduler.schedulers.base import (
    BaseScheduler,
)
from dishka import AsyncContainer, Container, Scope
from dishka.integrations.base import (
    InjectFunc,
    is_dishka_injected,
    wrap_injection,
)

from apscheduler_dishka.errors import (
    NotConfigureDishkaContainerError,
)
from apscheduler_dishka.executor import (
    DISHKA_CONTAINER_KEY,
    inject_executor,
)

P = ParamSpec("P")
T = TypeVar("T")


def inject(func: Callable[P, T]) -> Callable[P, T]:
    def container_getter(
            *args: P.args,
            **kwargs: P.kwargs,
    ) -> Container | AsyncContainer:
        job_kwargs: dict[str, Any] = cast(dict[str, Any], args[1])
        container = job_kwargs.get(
            DISHKA_CONTAINER_KEY,
        )
        if container is None:
            raise NotConfigureDishkaContainerError
        job_kwargs.pop(DISHKA_CONTAINER_KEY, None)
        return container  # type: ignore[no-any-return]

    return wrap_injection(  # type: ignore[call-overload, no-any-return]
        func=func,
        is_async=iscoroutinefunction(func),
        remove_depends=True,
        container_getter=container_getter,
        scope=Scope.REQUEST,
    )


def _inject_scheduler(
        scheduler: BaseScheduler,
        inject_func: InjectFunc[P, T],
) -> BaseScheduler:
    original_add_job = scheduler.add_job

    @wraps(scheduler.add_job)
    def _add_job(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Job:
        if not is_dishka_injected(func):
            func = inject_func(func)
        return original_add_job(func, *args, **kwargs)

    scheduler.add_job = _add_job
    return scheduler


def setup_dishka(
        container: AsyncContainer | Container,
        scheduler: BaseScheduler,
        *,
        auto_inject: bool | InjectFunc[P, T] = False,
) -> None:
    inject_func: InjectFunc[P, T] = inject

    if auto_inject is not False:
        if auto_inject is True:
            inject_func = inject
        else:
            inject_func = auto_inject

        _inject_scheduler(scheduler=scheduler, inject_func=inject_func)

    current_default_executor = scheduler._create_default_executor()  # noqa: SLF001
    scheduler._create_default_executor = lambda: inject_executor(  # noqa: SLF001
        executor=current_default_executor,
        dishka_container=container,
        inject_func=inject_func,
    )

    for executor in scheduler._executors.values():  # noqa: SLF001
        inject_executor(
            executor=executor,
            dishka_container=container,
            inject_func=inject_func,
        )
