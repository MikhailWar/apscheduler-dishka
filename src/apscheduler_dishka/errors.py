from dishka.exception_base import DishkaError


class NotConfigureDishkaContainerError(DishkaError):
    def __str__(self) -> str:
        return (
            "Dishka container is not configured. "
            "Use setup_dishka from apscheduler_dishka.integration"
        )


class FailedToInjectDishkaContainerError(DishkaError):
    def __init__(self, message: str) -> None:
        self._message = message

    def __str__(self) -> str:
        return self._message


class RunJobError(DishkaError):
    def __init__(self, message: str):
        self._message = message

    def __str__(self) -> str:
        return self._message
