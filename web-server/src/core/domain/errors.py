from dataclasses import dataclass
from enum import Enum
from typing import Any


class CoreErrorCategory(str, Enum):
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    INTERNAL_ERROR = "internal_error"


@dataclass(repr=False)
class CoreError(Exception):
    """
    Core domain exception. Kept strictly inside the domain layer
    to represent business rule violations and controlled failures.
    """

    message: str
    category: CoreErrorCategory = CoreErrorCategory.INTERNAL_ERROR
    detail: Any = None

    def __post_init__(self) -> None:
        super().__init__(self.message)

    @property
    def is_operational(self) -> bool:
        return self.category in (
            CoreErrorCategory.BAD_REQUEST,
            CoreErrorCategory.NOT_FOUND,
            CoreErrorCategory.CONFLICT,
        )

    def __repr__(self) -> str:
        return f"CoreError(category={self.category.value}, message={self.message})"
