from fastapi import APIRouter, Depends, Response, status

from adapters.inbound.http.controllers.v1.health.mapper import (
    HealthMapper,
    LivenessResponseSchema,
    ReadinessResponseSchema,
)
from adapters.inbound.http.dependencies.dependencies import (
    Dependencies,
)
from core.domain import HealthStatus
from core.ports.inbound.health_port import HealthCheckInputPort

health_router = APIRouter(prefix="/health")


@health_router.get(
    "/liveness",
    response_model=LivenessResponseSchema,
    summary="Check if the API process is running natively",
    status_code=status.HTTP_200_OK,
)
async def get_liveness_status() -> LivenessResponseSchema:
    """
    Shallow health check. It does not hit the database, message broker or any external
    dependency. It strictly validates that the Uvicorn/FastAPI process is responsive.
    If this endpoint fails, the infrastructure provider (Render/AWS) should RESTART the container.
    """
    return LivenessResponseSchema(status="healthy")


@health_router.get(
    "/readiness",
    response_model=ReadinessResponseSchema,
    summary="Check health of all active sub-systems and infrastructure resources",
)
async def get_readiness_status(
    response: Response,
    health_check_use_case: HealthCheckInputPort = Depends(
        Dependencies.health_check_use_case
    ),
) -> ReadinessResponseSchema:
    """
    Deep health check. Orchestrates network checks against MongoDB.
    If any dependency fails, it returns 503 Service Unavailable, signaling the Load Balancer
    to ISOLATE this container from public client traffic until it recovers.
    """
    health_domain = await health_check_use_case.get_health_status()

    if health_domain.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthMapper.domain_to_response(health_domain)
