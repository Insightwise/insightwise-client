import os

from client.session import Session
from client.exceptions import AuthenticationError
from warrant_lite import WarrantLite
import requests
import boto3


class AuthClient:

    def __init__(self, base_url):
        self._base_url = base_url

    def login_user(self, username: str, password: str, client_id: str, user_pool_id: str) -> Session:

        cognito_client = boto3.client("cognito-idp", region_name=os.environ["REGION"])
        try:
            srp = WarrantLite(
                username=username,
                password=password,
                pool_id=user_pool_id,
                client_id=client_id,
                client=cognito_client,
            )
            tokens = srp.authenticate_user()

            return Session(
                id_token=tokens["AuthenticationResult"]["IdToken"],
                access_token=tokens["AuthenticationResult"]["AccessToken"],
                refresh_token=tokens["AuthenticationResult"]["RefreshToken"],
                **self._get_me(tokens["AuthenticationResult"]["IdToken"])
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

