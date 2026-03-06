from dishka.exception_base import DishkaError


class NotConfigureDishkaContainerError(DishkaError):
    def __str__(self) -> str:
        return "Dishka container is not configured. Use setup_dishka from apscheduler_dishka.integration"
