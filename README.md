# APScheduler integration for Dishka

[![PyPI version](https://badge.fury.io/py/apscheduler-dishka.svg)](https://pypi.python.org/pypi/apscheduler-dishka)
[![Supported versions](https://img.shields.io/pypi/pyversions/apscheduler-dishka.svg)](https://pypi.python.org/pypi/apscheduler-dishka)
[![Downloads](https://img.shields.io/pypi/dm/apscheduler-dishka.svg)](https://pypistats.org/packages/apscheduler-dishka)
[![License](https://img.shields.io/github/license/MikhailWar/apscheduler-dishka)](https://github.com/MikhailWar/apscheduler-dishka/blob/main/LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/MikhailWar/apscheduler-dishka/setup.yml)](https://github.com/MikhailWar/apscheduler-dishka/actions)

This package provides integration of [Dishka](http://github.com/reagento/dishka/) dependency injection framework and [APScheduler](https://github.com/agronholm/apscheduler), an advanced Python scheduler.

## Installation

```sh
pip install apscheduler-dishka
```

## Features

* automatic *REQUEST* scope management for scheduled jobs
* automatic injection of dependencies into job functions
* support for both sync and async schedulers
* support for `auto_inject` mode to automatically wrap all jobs

## How to use

1. Import

```python
from apscheduler_dishka import (
    inject,
    setup_dishka,
)
from dishka import make_container, Provider, provide, Scope, FromDishka
```

2. Create provider

```python
class YourProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_interactor(self) -> Interactor:
         ...
```

3. Mark those of your job function parameters which are to be injected with `FromDishka[]` and decorate them using `@inject`

```python
@inject
def job(
    data: str,
    interactor: FromDishka[Interactor],
):
    ...
```

4. Create container

```python
container = make_container(YourProvider())
```

5. Setup `dishka` integration

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler_dishka import setup_dishka

scheduler = BlockingScheduler()
setup_dishka(container=container, scheduler=scheduler)
```

6. Add jobs to scheduler

```python
scheduler.add_job(
    job,
    trigger="interval",
    seconds=5,
    args=["args"],
)
```

## Auto-inject mode

If you don't want to manually decorate each job with `@inject`, you can use `auto_inject` mode:

```python
setup_dishka(
    container=container,
    scheduler=scheduler,
    auto_inject=True,
)
```

In this mode, all jobs will be automatically wrapped with dependency injection:

```python
def job(
    data: str,
    interactor: FromDishka[Interactor],
):
    ...

scheduler.add_job(
    job,
    trigger="interval",
    seconds=5,
    args=["args"],
)
```

## Async support

The library supports async schedulers:

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dishka import make_async_container
from apscheduler_dishka import setup_dishka

scheduler = AsyncIOScheduler()
container = make_async_container(YourProvider())
setup_dishka(container=container, scheduler=scheduler)
```
