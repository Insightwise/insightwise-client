from typing import List, Optional, Dict, Union
from pydantic import Field
from client.models import StringEnum, DatabaseModel, CoreModel


class DashboardFailureType(StringEnum):
    UNKNOWN = "UNKNOWN"
    THEMES = "THEMES"


class DashboardStatus(StringEnum):
    WAITING_FOR_FILES = "WAITING_FOR_FILES"
    CREATING_THEMES = "CREATING_THEMES"
    CONFIRM_THEMES = "CONFIRM_THEMES"
    THEMES_CONFIRMED = "THEMES_CONFIRMED"
    CREATING_INSIGHTS = "CREATING_INSIGHTS"
    LABELLING_DATA = "LABELLING_DATA"
    CREATING_THEME_DETAILS = "CREATING_THEME_DETAILS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class Dashboard(DatabaseModel):
    organisation_id: str
    project_id: str
    document_ids: List[str]
    name: str
    progress: float = 0
    progress_details: Optional[str] = None
    chunk_query: Optional[List[Dict]] = None
    status: DashboardStatus = DashboardStatus.WAITING_FOR_FILES
    failure_type: Optional[DashboardFailureType] = None
    retry_attempts: int = 0
    task_token: Optional[str] = None
    prompt_directions: Optional[str] = None
    allowed_regions: List[str] = Field(default_factory=lambda: ["ap-southeast-2"])
    preferred_language: str = "en-AU"
    total_unique_mentions: Optional[int] = None
    total_mentions: Optional[int] = None


class DashboardCreate(CoreModel):
    name: str
    document_ids: List[str]
    confirmed: bool = True


class DashboardUpdate(CoreModel):
    status: Optional[DashboardStatus] = None
