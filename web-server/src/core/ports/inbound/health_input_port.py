from abc import ABC, abstractmethod

from core.domain.health import Health


class HealthInputPort(ABC):
    @abstractmethod
    async def get_health_status(self) -> Health:
        pass
