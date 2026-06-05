from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.core.errors.core_error import CoreError, CoreErrorCategory
from src.core.logging.logger_factory import get_logger

logger = get_logger(__name__)


class HTTPExceptionHandler:
    _CATEGORY_MAP = {
        CoreErrorCategory.BAD_REQUEST: status.HTTP_400_BAD_REQUEST,
        CoreErrorCategory.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        CoreErrorCategory.CONFLICT: status.HTTP_409_CONFLICT,
        CoreErrorCategory.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    @classmethod
    async def handle_core_error(cls, request: Request, exc: CoreError) -> JSONResponse:
        status_code = cls._get_status_code(exc.category)

        content = {
            "error": True,
            "type": "core-error",
            "category": exc.category,
            "message": exc.message,
            "details": exc.detail,
        }

        logger.warning(
            f"Core Exception [{status_code}] on {request.method} {request.url.path} - {exc.message}"
        )
        return JSONResponse(content=content, status_code=status_code)

    @classmethod
    def _get_status_code(cls, category: str) -> int:
        return cls._CATEGORY_MAP.get(category, status.HTTP_500_INTERNAL_SERVER_ERROR)
