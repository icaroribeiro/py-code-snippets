from ports.inbound.health_input_port import HealthInputPort
from ports.outbound.health.health_service import HealthServicePort
from src.core.domain.health import Health
from src.adapters.inbound.http.mappers.health_mapper import HealthMapper
from src.core.logging.logger_factory import get_logger

logger = get_logger(__name__)


class CheckHealthUseCase(HealthInputPort):
    def __init__(self, health_service: HealthServicePort) -> None:
        self._health_service = health_service

    async def get_health_status(self) -> Health:
        logger.info("Executing global infrastructure health check validation...")
        
        services_status = await self._health_service.check_services_availability()
        
        health_domain = HealthMapper.services_to_domain(services_status)
        
        logger.info(f"Global system health resolved to: {health_domain.status}")
        return health_domain