from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from client.models import DatabaseModel


class Permission(BaseModel):
    user_id: str
    email: str
    role: str
    status: str


class Project(DatabaseModel):
    organisation_id: str
    name: str
    permissions: List[Permission]
    version: str
    status: str
    timestamp: datetime
    default_dashboard_id: Optional[str] = None


class ProjectCreate(BaseModel):
    name: str | None = "Untitled"
