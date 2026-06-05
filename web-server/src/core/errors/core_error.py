from typing import Any


class CoreErrorCategory:
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    INTERNAL_ERROR = "internal_error"


class CoreError(Exception):
    def __init__(
        self,
        message: str,
        category: str = CoreErrorCategory.INTERNAL_ERROR,
        detail: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.category = category
        self.detail = detail
        self.is_operational = category in (
            CoreErrorCategory.BAD_REQUEST,
            CoreErrorCategory.NOT_FOUND,
            CoreErrorCategory.CONFLICT,
        )

    def __repr__(self) -> str:
        return f"CoreError(category={self.category}, message={self.message})"
