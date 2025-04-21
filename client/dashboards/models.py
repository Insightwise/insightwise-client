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
    document_ids: list[str]
    name: str
    progress: float = 0
    progress_details: str | None = None
    chunk_query: list[dict] | None = None
    status: DashboardStatus = DashboardStatus.WAITING_FOR_FILES
    failure_type: DashboardFailureType | None = None
    retry_attempts: int = 0
    task_token: str | None = None
    prompt_directions: str | None = None
    allowed_regions: list[str] = Field(default_factory=lambda: ["ap-southeast-2"])
    preferred_language: str = "en-AU"
    total_unique_mentions: int | None = None
    total_mentions: int | None = None


class DashboardCreate(CoreModel):
    name: str
    document_ids: list[str]
    confirmed: bool = True


class DashboardUpdate(CoreModel):
    status: DashboardStatus | None = None

