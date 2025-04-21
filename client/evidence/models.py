from typing import Union, Optional, List, Set, Dict

from client.documents.models import DocumentType
from client.models import StringEnum, DatabaseModel, CoreModel
from pydantic import BaseModel, Field, field_serializer


class ChunkMetaType(StringEnum):
    NUMBER = "NUMBER"
    LABEL = "LABEL"
    ID = "ID"


class ChunkMeta(BaseModel):
    format_type: ChunkMetaType
    label: str
    value: str


class ChunkInsight(CoreModel):
    theme: Optional[str] = None
    insight: Optional[str] = None

    def __hash__(self):
        """Allows the model to be used in a set by hashing theme + insight."""
        return hash((self.theme, self.insight))

    def __eq__(self, other):
        """Ensures equality check is based on theme + insight."""
        if isinstance(other, ChunkInsight):
            return (self.theme, self.insight) == (other.theme, other.insight)
        return False


class Chunk(DatabaseModel):
    document_id: Optional[str]
    project_id: Optional[str] = None
    organisation_id: Optional[str] = None
    dashboard_id: Optional[str] = None
    speaker: Optional[str] = None
    speaker_id: Optional[str] = None
    is_interviewer: bool = False
    question: Optional[str] = None
    raw_text: Optional[str] = None
    document_name: Optional[str] = None
    document_type: Optional[DocumentType] = None
    chunk_meta: Optional[List[ChunkMeta]] = None
    related_insights: Set[ChunkInsight] = Field(default_factory=set)
    labels: Dict = Field(default_factory=dict)

    @field_serializer("related_insights")
    def serialize_related_insights(self, value: Set[str], _info) -> List[str]:
        # Convert set to list for JSON serialization
        return list(value)


class ChunkUpdate(BaseModel):
    related_insights: Set[ChunkInsight] = Field(default_factory=set)

    @field_serializer("related_insights")
    def serialize_related_insights(self, value: Set[str], _info) -> List[str]:
        # Convert set to list for JSON serialization
        return list(value)
