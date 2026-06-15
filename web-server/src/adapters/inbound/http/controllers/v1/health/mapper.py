from typing import Dict

from pydantic import BaseModel, Field

from core.domain.health import Health


class LivenessResponseSchema(BaseModel):
    status: str = Field("healthy", description="Indicates if the API process is alive")


class ReadinessResponseSchema(BaseModel):
    status: str = Field(...)
    services: Dict[str, str] = Field(...)
    verified_at: str = Field(...)


class HealthMapper:
    @staticmethod
    def domain_to_response(domain: Health) -> ReadinessResponseSchema:
        """
        Maps the pure domain entity to the HTTP Inbound Response Schema.
        Used strictly at the API controller border.
        """
        return ReadinessResponseSchema(
            status=domain.status,
            services=domain.services,
            verified_at=domain.verified_at.isoformat().replace("+00:00", "") + "Z",
        )
