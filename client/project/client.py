from client.base_client import BaseClient
from client.project.models import Project, ProjectCreate


class ProjectClient(BaseClient[Project, ProjectCreate, Project]):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            endpoint="/v1/organisations/{organisation_id}/projects",
            model=Project,
            create_model=ProjectCreate,
            update_model=Project,
        )
