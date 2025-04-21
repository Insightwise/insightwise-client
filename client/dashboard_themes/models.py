from typing import List, Optional, Union
from client.models import StringEnum, DatabaseModel, CoreModel


class DashboardThemeStatus(StringEnum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class DashboardThemeFailureType(StringEnum):
    UNKNOWN = "UNKNOWN"
    LLM = "LLM"


class DashboardThemeInsight(CoreModel):
    title: str
    description: str


class DashboardTheme(DatabaseModel):
    id: Optional[str] = None
    organisation_id: str
    project_id: str
    dashboard_id: str
    theme: str
    description: str
    insights: Optional[List[DashboardThemeInsight]] = None
    unique_documents: Optional[int] = None
    unique_mentions: Optional[int] = None
    mentions: Optional[int] = None
    status: DashboardThemeStatus = DashboardThemeStatus.CREATED
    progress_details: Optional[str] = None
    failure_type: Optional[DashboardThemeFailureType] = None


class DashboardThemeUpdate(CoreModel):
    theme: str
    description: str
