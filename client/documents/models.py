from typing import Optional
from pydantic import BaseModel

from client.models import DatabaseModel, StringEnum, CoreModel


class DocumentType(StringEnum):
    TEXT = "TEXT"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    TABULAR = "TABULAR"
    TRANSCRIPT = "TRANSCRIPT"
    UNKNOWN = "UNKNOWN"


class DocumentFailureType(StringEnum):
    GENERAL = "GENERAL"
    VIDEO_PROCESSING = "VIDEO_PROCESSING"
    AUDIO_PROCESSING = "AUDIO_PROCESSING"
    EMPTY = "EMPTY"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    TRANSCRIPT = "TRANSCRIPT"
    THEMES = "THEMES"
    UPLOAD = "UPLOAD"
    UNKNOWN = "UNKNOWN"
    INSUFFICIENT_CREDITS = "INSUFFICIENT_CREDITS"


class DocumentStatus(StringEnum):
    CREATED = "CREATED"
    UPLOADED = "UPLOADED"
    CONFIRMING_CREDITS = "CONFIRMING_CREDITS"
    PROCESSING = "PROCESSING"
    WAITING = "WAITING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class Participant(BaseModel):
    reference: str
    name: str | None = None
    role: str | None = None
    is_interviewer: bool = False
    additional: dict | None = None


class File(BaseModel):
    name: str
    content_type: str
    url: str


class Document(DatabaseModel):
    name: str
    organisation_id: str
    project_id: str | None = None
    status: DocumentStatus = DocumentStatus.CREATED
    size: float | None = None
    url: str | None = None
    credit_cost: float | None = None
    progress_details: Optional[str] = None
    progress: float = 0
    participants: list[Participant] | None = None
    transcript_file: Optional[File] = None
    document_type: DocumentType | None = None
    failure_type: Optional[DocumentFailureType] = None
    confirmed: bool | None = None


class DocumentCreate(CoreModel):
    name: str
    content_type: str | None = None
    size: int = 0


class DocumentUpdate(CoreModel):
    status: DocumentStatus | None = None
    confirmed: bool | None = None
