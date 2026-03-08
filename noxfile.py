import sys
from collections.abc import Callable
from dataclasses import dataclass

import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

EDITABLE_INSTALL = ("-e", ".")


@dataclass(frozen=True, slots=True)
class Constraint:
    reason: str = ""
    condition: Callable[[], bool] = lambda: True


@dataclass(frozen=True, slots=True)
class IntegrationEnv:
    library: str
    version: str
    folder_path: str
    constraint: Constraint | None = None

    def get_req(self) -> str:
        return (
            f"requirements/{self.library.replace('_', '-')}"
            f"-{self.version}.txt"
        )

    def get_tests(self) -> str:
        return f"tests/scheduler/{self.folder_path}"


def python_version_less(*version: int) -> Constraint:
    version_str = ".".join(map(str, version))
    return Constraint(
        f"Skip tests on python {version_str} due to compatibility issues",
        lambda: sys.version_info < version,
    )


INTEGRATIONS = [
    IntegrationEnv(
        library="gevent",
        version="latest",
        folder_path="integrations/gevent",
    ),
    IntegrationEnv(
        library="qt",
        version="latest",
        folder_path="integrations/qt",
    ),
    IntegrationEnv(
        library="redis",
        version="latest",
        folder_path="integrations/redis_jobstore",
    ),
    IntegrationEnv(
        library="tornado",
        version="latest",
        folder_path="integrations/tornado",
    ),
    IntegrationEnv(
        library="twisted",
        version="latest",
        folder_path="integrations/twisted",
    ),
]




@nox.session(tags=["ci"])
def unit(session: nox.Session) -> None:
    session.install(
        *EDITABLE_INSTALL,
        "-r", "requirements/test.txt",
        silent=False,
    )
    session.run("pytest", "tests/unit")


@nox.session(tags=["ci"])
def scheduler_core(session: nox.Session) -> None:
    session.run("pytest", "tests/scheduler/core")


for env in INTEGRATIONS:
    @nox.session(
        name=f"{env.library}_{env.version}",
        tags=["ci"],
    )
    def scheduler_integration(session: nox.Session, env=env) -> None:
        if env.constraint and not env.constraint.condition():
            session.skip(env.constraint.reason)

        session.install(*EDITABLE_INSTALL, "-r", env.get_req(), silent=False)
        session.run("pytest", env.get_tests())
