from dataclasses import dataclass
from datetime import datetime
from typing import Dict


class HealthStatus:
    HEALTHY = "Healthy"
    UNHEALTHY = "Unhealthy"


@dataclass(frozen=True)
class Health:
    status: str
    services: Dict[str, str]
    verified_at: datetime
