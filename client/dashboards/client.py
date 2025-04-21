from client.base_client import BaseClient
from client.dashboards.models import Dashboard, DashboardCreate, DashboardUpdate


class DashboardClient(BaseClient[Dashboard, DashboardCreate, DashboardUpdate]):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            endpoint="/v3/organisations/{organisation_id}/projects/{project_id}/dashboards",
            model=Dashboard,
            create_model=DashboardCreate,
            update_model=DashboardUpdate,
            require_ids=["project_id"]
        )
