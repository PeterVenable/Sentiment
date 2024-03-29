from authlib.oauth2.rfc6750 import BearerTokenValidator

from authentication.storage import TokenStorage


class Validator(BearerTokenValidator):

    def __init__(self, storage: TokenStorage, **extra_attributes):
        super().__init__(**extra_attributes)
        self.storage = storage

    def authenticate_token(self, token_string):
        return self.storage.get_token(token_string)
