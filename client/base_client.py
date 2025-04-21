import json
from typing import Generic, Type, TypeVar, Optional
from pydantic import BaseModel
import requests

from client.session import Session
from client.models import PaginatedResponse

T = TypeVar("T", bound=BaseModel)  # Response model
C = TypeVar("C", bound=BaseModel)  # Create model
U = TypeVar("U", bound=BaseModel)  # Update model


class BaseClient(Generic[T, C, U]):

    def __init__(
        self,
        base_url: str,
        session: Session,
        endpoint: str,
        model: Type[T],
        create_model: Type[C],
        update_model: Type[U],
        require_ids: list = None
    ):
        self._base_url = base_url
        self._session = session
        self._endpoint = endpoint
        self._model = model
        self._create_model = create_model
        self._update_model = update_model
        self._require_ids = require_ids

    def _build_url(self, path: Optional[str] = "", **kwargs) -> str:
        for id_name in self._require_ids or []:
            id_value = kwargs.get(id_name)
            if not id_value:
                raise ValueError(f"{id_name} is required for this operation")

        # Always include organisation_id from the session
        params = {"organisation_id": self._session.organisation_id, **kwargs}
        base = self._endpoint.format(**params)
        return f"{self._base_url}{base}{path}"

    def list(self, query_params: dict = None, **url_params) -> PaginatedResponse[T]:
        res = requests.get(
            url=self._build_url(**url_params),
            headers=self._session.headers,
            params=self._stringify_query_params(query_params) or {},
        )
        return PaginatedResponse[self._model].model_validate(res.json())

    def create(self, data: C, **url_params) -> T:
        res = requests.post(
            url=self._build_url(**url_params),
            headers=self._session.headers,
            json=data.model_dump(),
        )
        return self._model.model_validate(res.json())

    def get(self, item_id: str, **url_params) -> T:
        res = requests.get(
            url=self._build_url(f"/{item_id}", **url_params),
            headers=self._session.headers,
        )
        return self._model.model_validate(res.json())

    def update(self, item_id: str, data: U, **url_params) -> T:
        res = requests.patch(
            url=self._build_url(f"/{item_id}", **url_params),
            headers=self._session.headers,
            json=data.model_dump(),
        )
        return self._model.model_validate(res.json())

    def delete(self, item_id: str, **url_params) -> None:
        requests.delete(
            url=self._build_url(f"/{item_id}", **url_params),
            headers=self._session.headers,
        )

    @staticmethod
    def _stringify_query_params(query_params: dict) -> dict:
        return {
            key: json.dumps(value) if isinstance(value, (list, dict)) else value
            for key, value in (query_params or {}).items()
        }
