from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable, ParamSpec, TypeVar, Container

from apscheduler.schedulers.base import BaseScheduler
from dishka import AsyncContainer, Scope
from dishka.integrations.base import wrap_injection, is_dishka_injected, InjectFunc

from apscheduler_dishka.errors import NotConfigureDishkaContainerError
from apscheduler_dishka.executor import DishkaSchedulerExecutor, DISHKA_CONTAINER_KEY

P = ParamSpec("P")
T = TypeVar("T")




def inject(func: Callable[P, T]) -> Callable[P, T]:
    def container_getter(*args, **kwargs):
        job_kwargs: dict = args[1]
        container: Container | AsyncContainer = job_kwargs.get(DISHKA_CONTAINER_KEY)
        if container is None:
            raise NotConfigureDishkaContainerError()
        job_kwargs.pop(DISHKA_CONTAINER_KEY, None)
        return container

    return wrap_injection(
        func=func,
        is_async=iscoroutinefunction(func),
        remove_depends=True,
        container_getter=container_getter,
        scope=Scope.REQUEST,
    )


def _add_job_inject(function: Callable[P, T], inject_func: InjectFunc[P, T]):
    @wraps(function)
    def wrapper(
            func: Callable[P, T],
            *args: P.args,
            **kwargs: P.kwargs
    ) -> T:
        if not is_dishka_injected(func):
            func = inject_func(func)
        return function(func, *args, **kwargs)

    return wrapper


def setup_dishka(
        container: AsyncContainer | Container,
        scheduler: BaseScheduler,
        auto_inject: bool | InjectFunc[P, T] = False,
):

    dishka_executor = DishkaSchedulerExecutor(
        inject_func=inject,
        dishka_container=container,
    )

    if auto_inject is not False:
        inject_func: InjectFunc[P, T]
        if auto_inject is True:
            inject_func = inject
        else:
            inject_func = auto_inject
        scheduler.add_job = _add_job_inject(scheduler.add_job, inject_func)
        dishka_executor = DishkaSchedulerExecutor(
            inject_func=inject,
            dishka_container=container,
        )

    scheduler.add_executor(dishka_executor, alias="default")
