# from authlib.oauth2.rfc6749 import ClientMixin
import time

from authlib.integrations.sqla_oauth2 import OAuth2TokenMixin


class Token(OAuth2TokenMixin):
    def __init__(self, client_id: str, access_token: str = ""):
        self.client_id = client_id
        self.token_type = "Bearer"
        self.access_token = access_token
        self.refresh_token = None
        self.scope = ""
        self.issued_at = int(time.time())
        self.access_token_revoked_at = 0
        self.refresh_token_revoked_at = 0
        self.expires_in = 0
