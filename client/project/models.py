from datetime import datetime
from typing import List, Optional

from client.models import DatabaseModel, CoreModel


class Permission(CoreModel):
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


class ProjectCreate(CoreModel):
    name: Optional[str] = "Untitled"
    ui_version: Optional[int] = 2
