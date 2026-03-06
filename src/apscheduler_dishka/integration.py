from collections.abc import Callable
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, ParamSpec, TypeVar, cast

from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler,
)
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
    FailedToSetupDishkaContainerError,
    NotConfigureDishkaContainerError,
)
from apscheduler_dishka.executor import (
    DISHKA_CONTAINER_KEY,
    AsyncDishkaSchedulerExecutor,
    DishkaSchedulerExecutor,
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


def _add_job_inject(
        function: Callable[..., Any],
        inject_func: Callable[..., Any],
) -> Callable[..., Any]:
    @wraps(function)
    def wrapper(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        if not is_dishka_injected(func):
            func = inject_func(func)
        return function(func, *args, **kwargs)

    return wrapper


def create_executor(
        scheduler: BaseScheduler,
        dishka_container: AsyncContainer | Container,
        inject_func: InjectFunc[P, T],

) -> DishkaSchedulerExecutor | AsyncDishkaSchedulerExecutor:
    if (
            not isinstance(scheduler, AsyncIOScheduler)
            and isinstance(dishka_container, AsyncContainer)
    ):
        raise FailedToSetupDishkaContainerError(
            message="AsyncContainer can be used only with AsyncIOScheduler",
        )

    if isinstance(dishka_container, AsyncContainer):
        return AsyncDishkaSchedulerExecutor(
            inject_func=inject_func,
            dishka_container=dishka_container,
        )

    return DishkaSchedulerExecutor(
        inject_func=inject_func,
        dishka_container=dishka_container,
    )


def setup_dishka(
        container: AsyncContainer | Container,
        scheduler: BaseScheduler,
        *,
        auto_inject: bool | InjectFunc[P, T] = False,
) -> None:
    dishka_executor = create_executor(
        scheduler=scheduler,
        dishka_container=container,
        inject_func=inject,
    )

    if auto_inject is not False:
        inject_func: InjectFunc[P, T]
        if auto_inject is True:
            inject_func = inject
        else:
            inject_func = auto_inject
        scheduler.add_job = _add_job_inject(scheduler.add_job, inject_func)
        dishka_executor = create_executor(
            scheduler=scheduler,
            dishka_container=container,
            inject_func=inject,
        )

    scheduler.add_executor(dishka_executor, alias="default")
