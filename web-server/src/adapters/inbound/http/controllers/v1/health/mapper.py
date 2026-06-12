from typing import Dict

from pydantic import BaseModel, Field

from core.domain.health import Health


class HealthResponseSchema(BaseModel):
    status: str = Field(...)
    services: Dict[str, str] = Field(...)
    verified_at: str = Field(...)


class HealthMapper:
    @staticmethod
    def domain_to_response(domain: Health) -> HealthResponseSchema:
        """
        Maps the pure domain entity to the HTTP Inbound Response Schema.
        Used strictly at the API controller border.
        """
        return HealthResponseSchema(
            status=domain.status,
            services=domain.services,
            verified_at=domain.verified_at.isoformat().replace("+00:00", "") + "Z",
        )
