from datetime import datetime, timezone

from core.domain.health import Health, HealthStatus
from core.ports.inbound.health.input_port import HealthInputPort
from core.ports.outbound.health.checker_output_port import HealthCheckerOutputPort
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class HealthUseCase(HealthInputPort):
    def __init__(self, health_checker: HealthCheckerOutputPort) -> None:
        self._health_checker = health_checker

    async def get_health_status(self) -> Health:
        logger.info("Executing global infrastructure health check validation...")

        services_status = await self._health_checker.check_services_availability()

        is_healthy = all(
            status.lower() == HealthStatus.HEALTHY.lower()
            for status in services_status.values()
        )
        logger.info("is_healthy resolved to: %s", is_healthy)
        global_status = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY

        health_domain = Health(
            status=global_status,
            services=services_status,
            verified_at=datetime.now(timezone.utc),
        )

        logger.info(f"Global systems health resolved to: {health_domain.status}")
        return health_domain
