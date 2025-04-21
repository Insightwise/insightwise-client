from enum import Enum
from typing import Optional, TypeVar, Generic, Any
from typing_extensions import Self

from pydantic import BaseModel
from humps import decamelize, camelize


class StringEnum(str, Enum):
    def __str__(self):
        return self.value


class CoreModel(BaseModel):

    @classmethod
    def model_validate(cls, obj, *args, **kwargs) -> Self:
        return super().model_validate(decamelize(obj), *args, **kwargs)

    def model_dump(self, *args, **kwargs) -> dict:
        data = super().model_dump(*args, **kwargs)
        return camelize(data)


class DatabaseModel(CoreModel):
    id: str


class PaginationLinks(BaseModel):
    next: Optional[str] = None
    previous: Optional[str] = None
    first: str
    last: str


T = TypeVar("T", bound=DatabaseModel)


class PaginatedResponse(BaseModel, Generic[T]):
    results: list[T]
    page: int
    limit: int
    total_items: int
    total_pages: int
    links: PaginationLinks

    @classmethod
    def model_validate(cls, obj: Any, *args, **kwargs) -> Self:
        return super().model_validate(decamelize(obj), *args, **kwargs)
