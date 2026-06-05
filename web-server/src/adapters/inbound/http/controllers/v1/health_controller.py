from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from src.adapters.inbound.http.mappers.health_mapper import (
    HealthMapper,
    HealthResponseSchema,
)
from src.core.domain.health import HealthStatus
from src.core.usecase.check_health_usecase import CheckHealthUseCase
from src.infrastructure.container import Container

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponseSchema,
    summary="Check applications and dependencies vitals",
)
@inject
async def check_health(
    response: Response,
    check_health_usecase: CheckHealthUseCase = Depends(
        Provide[Container.check_health_usecase]
    ),
) -> HealthResponseSchema:
    health_domain = await check_health_usecase.get_health_status()

    if health_domain.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthMapper.domain_to_response(health_domain)
