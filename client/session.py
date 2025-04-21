from pydantic import BaseModel


class Session(BaseModel):
    id_token: str
    access_token: str
    refresh_token: str | None = None
    user_id: str | None = None
    organisation_id: str | None = None

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.id_token}",
            "Content-Type": "application/json"
        }
