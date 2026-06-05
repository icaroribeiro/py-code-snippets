from datetime import datetime, timezone
from typing import Dict
from pydantic import BaseModel, Field

from src.core.domain.health import Health, HealthStatus


class HealthResponseSchema(BaseModel):
    status: str = Field(...)
    services: Dict[str, str] = Field(...)
    verified_at: str = Field(...)


class HealthMapper:
    @staticmethod
    def services_to_domain(services: Dict[str, str]) -> Health:
        global_status = (
            HealthStatus.HEALTHY
            if all(s == HealthStatus.HEALTHY for s in services.values())
            else HealthStatus.UNHEALTHY
        )
        
        return Health(
            status=global_status,
            services=services,
            verified_at=datetime.now(timezone.utc)
        )

    @staticmethod
    def domain_to_response(health_domain: Health) -> HealthResponseSchema:
        return HealthResponseSchema(
            status=health_domain.status,
            services=health_domain.services,
            verified_at=health_domain.verified_at.isoformat().replace("+00:00", "") + "Z",
        )