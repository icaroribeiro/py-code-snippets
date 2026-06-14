from abc import ABC, abstractmethod

from core.domain.health import Health


class HealthCheckInputPort(ABC):
    @abstractmethod
    async def get_health_status(self) -> Health:
        pass
