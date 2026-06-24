from abc import ABC, abstractmethod
from typing import Dict


class HealthCheckOutputPort(ABC):
    @abstractmethod
    async def check_services_availability(self) -> Dict[str, str]:
        pass
