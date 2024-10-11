import msal
import reflex as rx
from typing import Dict, List, Optional
import os

ENV_VAR_CLIENT_ID = "AZURE_CLIENT_ID"
ENV_VAR_CLIENT_SECRET = "AZURE_CLIENT_SECRET"
ENV_VAR_TENANT_ID = "AZURE_TENANT_ID"

if not os.getenv(ENV_VAR_CLIENT_ID):
    raise Exception(f"Please set {ENV_VAR_CLIENT_ID} environment variable.")

if not os.getenv(ENV_VAR_CLIENT_SECRET):
    raise Exception(f"Please set {ENV_VAR_CLIENT_SECRET} environment variable.")

if not os.getenv(ENV_VAR_TENANT_ID):
    raise Exception(f"Please set {ENV_VAR_TENANT_ID} environment variable.")

client_id: str = os.environ.get(ENV_VAR_CLIENT_ID)
client_secret: str = os.environ.get(ENV_VAR_CLIENT_SECRET)
tenant_id: str = os.environ.get(ENV_VAR_TENANT_ID)
authority = f"https://login.microsoftonline.com/{tenant_id}"
login_redirect = "/home"
cache = msal.TokenCache()

sso_app: msal.ClientApplication
if client_secret:
    sso_app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority,
        token_cache=cache,
    )
else:
    sso_app = msal.PublicClientApplication(
        client_id=client_id,
        authority=authority,
        token_cache=cache,
    )


class SsoState(rx.State):
    _access_token: str = ""
    _flow: dict
    _token: Dict[str, str] = {}

    def redirect_sso(self) -> rx.Component:
        self._flow = sso_app.initiate_auth_code_flow(
            scopes=[], redirect_uri=f"{self.router.page.host}/callback"
        )
        return rx.redirect(self._flow["auth_uri"])

    def require_auth(self):
        if not self._token:
            return self.redirect_sso()

    @rx.var(cache=True)
    def check_auth(self) -> bool:
        return True if self._token else False

    @rx.var(cache=True)
    def token(self) -> Dict[str, str]:
        return self._token

    def logout(self):
        self._token = {}
        return rx.redirect(authority + "/oauth2/v2.0/logout")

    def callback(self):
        query_components = self.router.page.params

        auth_response = {
            "code": query_components.get("code"),
            "client_info": query_components.get("client_info"),
            "state": query_components.get("state"),
            "session_state": query_components.get("session_state"),
            "client-secret": client_secret,
        }
        try:
            result = sso_app.acquire_token_by_auth_code_flow(
                self._flow, auth_response, scopes=[]
            )
        except Exception as e:
            return rx.toast(f"error something went wrong")
        # this can be used for accessing graph
        self._access_token = result.get("access_token")
        self._token = result.get("id_token_claims")
        return rx.redirect(login_redirect)
