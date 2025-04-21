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
    id: str | None = None
    organisation_id: str
    project_id: str
    dashboard_id: str
    theme: str
    description: str
    insights: list[DashboardThemeInsight] | None = None
    unique_documents: int | None = None
    unique_mentions: int | None = None
    mentions: int | None = None
    status: DashboardThemeStatus = DashboardThemeStatus.CREATED
    progress_details: str | None = None
    failure_type: DashboardThemeFailureType | None = None


class DashboardThemeUpdate(CoreModel):
    theme: str
    description: str
