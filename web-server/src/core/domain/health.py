from datetime import datetime, timezone
from typing import Dict


class HealthStatus:
    HEALTHY = "Healthy"
    UNHEALTHY = "Unhealthy"


class Health:
    """Pure core domain structure representing system vitals."""

    def __init__(
        self, status: str, services: Dict[str, str], verified_at: datetime
    ) -> None:
        self.status = status
        self.services = services  # Ex: {"mongodb": "Healthy", "redis": "Healthy", ...}
        self.verified_at = verified_at

    @classmethod
    def create(cls, services: Dict[str, str]) -> "Health":
        """Domain Factory function."""
        # Se qualquer serviço falhar, o status global consolidado cai
        global_status = (
            HealthStatus.HEALTHY
            if all(s == HealthStatus.HEALTHY for s in services.values())
            else HealthStatus.UNHEALTHY
        )
        return cls(
            status=global_status, services=services, verified_at=datetime.now(timezone.utc)
        )
