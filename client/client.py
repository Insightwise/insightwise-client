import os
from typing import Union

from client.auth.client import AuthClient
from client.dashboard_themes.client import DashboardThemeClient
from client.dashboards.client import DashboardClient
from client.documents.client import DocumentClient
from client.evidence.client import EvidenceClient
from client.exceptions import AuthenticationError
from client.insights.client import InsightClient
from client.project.client import ProjectClient


def require_auth(attr_name):
    def decorator(func):
        @property
        def wrapper(self):
            value = getattr(self, attr_name, None)
            if value is None:
                raise AuthenticationError(f"You must call `authenticate()` before accessing `{func.__name__}`.")
            return value
        return wrapper
    return decorator


class Client:

    def __init__(self):
        self.session = None
        self._client_id = os.environ["CLIENT_ID"]
        self._user_pool_id = os.environ["USER_POOL_ID"]
        self._base_url = os.environ["BASE_URL"]
        self.auth = AuthClient(base_url=self._base_url)
        self._projects: Union[ProjectClient, None] = None
        self._documents: Union[DocumentClient, None] = None
        self._dashboards: Union[DashboardClient, None] = None
        self._insights: Union[InsightClient, None] = None
        self._dashboard_themes: Union[DashboardThemeClient, None] = None
        self._evidence: Union[EvidenceClient, None] = None

    def authenticate(self, username, password):
        self.session = self.auth.login_user(
            username,
            password,
            client_id=self._client_id,
            user_pool_id=self._user_pool_id,
        )
        self._projects = ProjectClient(base_url=self._base_url, session=self.session)
        self._documents = DocumentClient(base_url=self._base_url, session=self.session)
        self._dashboards = DashboardClient(base_url=self._base_url, session=self.session)
        self._insights = InsightClient(base_url=self._base_url, session=self.session)
        self._dashboard_themes = DashboardThemeClient(base_url=self._base_url, session=self.session)
        self._evidence = EvidenceClient(base_url=self._base_url, session=self.session)
        return self

    @require_auth('_projects')
    def projects(self):
        pass

    @require_auth('_documents')
    def documents(self):
        pass

    @require_auth('_dashboards')
    def dashboards(self):
        pass

    @require_auth('_insights')
    def insights(self):
        pass

    @require_auth('_dashboard_themes')
    def dashboard_themes(self):
        pass

    @require_auth('_evidence')
    def evidence(self):
        pass

