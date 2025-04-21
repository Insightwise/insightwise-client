from typing import Optional, List
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
    chunk_ids: List[str]


class Insight(DatabaseModel):
    organisation_id: str
    project_id: str
    dashboard_id: str
    dashboard_theme_id: str
    title: str
    description: str
    summary: Optional[str] = None
    details: Optional[List[InsightDetail]] = None
    unique_documents: Optional[int] = None
    unique_mentions: Optional[int] = None
    mentions: Optional[int] = None
    ordered_evidence: List[str] = Field(default_factory=list)
    status: InsightCardStatus = InsightCardStatus.CREATED
    progress_details: Optional[str] = None
    failure_type: Optional[InsightCardFailureType] = None
    evidence_changes: int = 0


class InsightUpdate(CoreModel):
    title: str
    description: str
    summary: Optional[str] = None
    details: Optional[List[InsightDetail]] = None
