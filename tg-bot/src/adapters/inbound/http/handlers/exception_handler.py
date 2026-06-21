from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.domain import CoreError, CoreErrorCategory
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class HTTPExceptionHandler:
    _CATEGORY_MAP = {
        CoreErrorCategory.BAD_REQUEST: status.HTTP_400_BAD_REQUEST,
        CoreErrorCategory.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        CoreErrorCategory.CONFLICT: status.HTTP_409_CONFLICT,
        CoreErrorCategory.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    @staticmethod
    async def handle_core_error(request: Request, exc: CoreError) -> JSONResponse:
        if not isinstance(exc, CoreError):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": True,
                    "type": "system-error",
                    "message": "An unexpected systemic error occurred.",
                },
            )

        status_code = HTTPExceptionHandler._CATEGORY_MAP.get(
            exc.category, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        content = {
            "error": True,
            "type": "core-error",
            "category": exc.category.value
            if hasattr(exc.category, "value")
            else str(exc.category),
            "message": exc.message,
            "details": exc.detail,
        }

        logger.warning(
            f"Core Exception [{status_code}] on {request.method} {request.url.path} - {exc.message}"
        )
        return JSONResponse(content=content, status_code=status_code)

    @staticmethod
    async def handle_http_exception(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        if not isinstance(exc, HTTPException):
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = str(exc)
        else:
            status_code = exc.status_code
            detail = exc.detail

        return JSONResponse(
            status_code=status_code,
            content={"error": True, "type": "http-error", "message": detail},
        )

    @staticmethod
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        if not isinstance(exc, RequestValidationError):
            errors_detail = None
        else:
            errors_detail = exc.errors()

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": True,
                "type": "validation-error",
                "details": errors_detail,
            },
        )
