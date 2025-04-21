from client.base_client import BaseClient
from client.insights.models import Insight, InsightUpdate


class InsightClient(BaseClient[Insight, Insight, Insight]):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            endpoint=(
                "/v3/organisations/{organisation_id}/projects/{project_id}/dashboards/{dashboard_id}/insight-cards"
            ),
            model=Insight,
            create_model=Insight,
            update_model=InsightUpdate,
            require_ids=["project_id", "dashboard_id"]
        )
