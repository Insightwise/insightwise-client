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
    theme: str | None = None
    insight: str | None = None

    def __hash__(self):
        """Allows the model to be used in a set by hashing theme + insight."""
        return hash((self.theme, self.insight))

    def __eq__(self, other):
        """Ensures equality check is based on theme + insight."""
        if isinstance(other, ChunkInsight):
            return (self.theme, self.insight) == (other.theme, other.insight)
        return False


class Chunk(DatabaseModel):
    document_id: str | None
    project_id: str | None = None
    organisation_id: str | None = None
    dashboard_id: str | None = None
    speaker: str | None = None
    speaker_id: str | None = None
    is_interviewer: bool = False
    question: str | None = None
    raw_text: str | None = None
    document_name: str | None = None
    document_type: DocumentType | None = None
    chunk_meta: list[ChunkMeta] | None = None
    related_insights: set[ChunkInsight] = Field(default_factory=set)
    labels: dict = Field(default_factory=dict)

    @field_serializer("related_insights")
    def serialize_related_insights(self, value: set[str], _info) -> list[str]:
        # Convert set to list for JSON serialization
        return list(value)


class ChunkUpdate(BaseModel):
    related_insights: set[ChunkInsight] = Field(default_factory=set)

    @field_serializer("related_insights")
    def serialize_related_insights(self, value: set[str], _info) -> list[str]:
        # Convert set to list for JSON serialization
        return list(value)
