from client.base_client import BaseClient
from client.dashboard_themes.models import DashboardTheme, DashboardThemeUpdate


class DashboardThemeClient(BaseClient[DashboardTheme, DashboardTheme, DashboardThemeUpdate]):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            endpoint=(
                "/v3/organisations/{organisation_id}/projects/{project_id}/dashboards/{dashboard_id}/dashboard-themes"
            ),
            model=DashboardTheme,
            create_model=DashboardTheme,
            update_model=DashboardThemeUpdate,
            require_ids=["project_id", "dashboard_id"]
        )
