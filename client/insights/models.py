from client.models import StringEnum, DatabaseModel, CoreModel
from pydantic import Field


class InsightCardStatus(StringEnum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class InsightCardFailureType(StringEnum):
    UNKNOWN = "UNKNOWN"
    LLM = "LLM"


class InsightDetail(CoreModel):
    statement: str
    chunk_ids: list[str]


class Insight(DatabaseModel):
    organisation_id: str
    project_id: str
    dashboard_id: str
    dashboard_theme_id: str
    title: str
    description: str
    summary: str | None = None
    details: list[InsightDetail] | None = None
    unique_documents: int | None = None
    unique_mentions: int | None = None
    mentions: int | None = None
    ordered_evidence: list[str] = Field(default_factory=list)
    status: InsightCardStatus = InsightCardStatus.CREATED
    progress_details: str | None = None
    failure_type: InsightCardFailureType | None = None
    evidence_changes: int = 0


class InsightUpdate(CoreModel):
    title: str
    description: str
    summary: str | None = None
    details: list[InsightDetail] | None = None
