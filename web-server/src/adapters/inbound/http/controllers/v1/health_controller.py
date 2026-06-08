from fastapi import APIRouter, Depends, Response, status

from adapters.inbound.http.dependencies.dependencies import (
    Dependencies,  # <-- Importa as dependências HTTP
)
from adapters.inbound.http.mappers.health_mapper import (
    HealthMapper,
    HealthResponseSchema,
)
from core.domain.health import HealthStatus
from core.use_cases.health_use_case import HealthUseCase

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponseSchema,
    summary="Check applications and dependencies vitals",
)
async def get_health_status(
    response: Response,
    health_use_case: HealthUseCase = Depends(Dependencies.health_use_case),
) -> HealthResponseSchema:
    health_domain = await health_use_case.get_health_status()

    if health_domain.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthMapper.domain_to_response(health_domain)
