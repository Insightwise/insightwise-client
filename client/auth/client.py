from client.session import Session
from client.exceptions import AuthenticationError
from warrant import Cognito
import requests


class AuthClient:

    def __init__(self, base_url):
        self._base_url = base_url

    def login_user(self, username: str, password: str, client_id: str, user_pool_id: str) -> Session:

        try:
            cognito = Cognito(
                user_pool_id=user_pool_id,
                client_id=client_id,
                username=username,
            )

            cognito.authenticate(password=password)

            return Session(
                id_token=cognito.id_token,
                access_token=cognito.access_token,
                refresh_token=cognito.refresh_token,
                **self._get_me(cognito.id_token)
            )

        except Exception as e:
            raise AuthenticationError(f"Login failed: {str(e)}")

    def _get_me(self, id_token: str):
        res = requests.get(
            f"{self._base_url}/v1/me",
            headers={
                "Authorization": f"Bearer {id_token}",
                "Content-Type": "application/json"
            }
        )
        data = res.json()
        return dict(user_id=data["id"], organisation_id=data["organisationId"])

