from client.base_client import BaseClient
from client.evidence.models import Chunk, ChunkUpdate


class EvidenceClient(BaseClient[Chunk, Chunk, ChunkUpdate]):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            endpoint=(
                "/v3/organisations/{organisation_id}/projects/{project_id}/dashboards/{dashboard_id}/evidence"
            ),
            model=Chunk,
            create_model=Chunk,
            update_model=ChunkUpdate,
            require_ids=["project_id", "dashboard_id"]
        )
