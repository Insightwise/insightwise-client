from typing import Optional

from pydantic import BaseModel


class Session(BaseModel):
    id_token: str
    access_token: str
    refresh_token: Optional[str] = None
    user_id: Optional[str] = None
    organisation_id: Optional[str] = None

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.id_token}",
            "Content-Type": "application/json"
        }
