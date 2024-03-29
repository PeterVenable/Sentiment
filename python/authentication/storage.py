from typing import Optional

from authlib.oauth2.rfc6749 import TokenMixin


class TokenStorage:
    def get_token(self, token_string: str) -> Optional[TokenMixin]:
        raise NotImplementedError()

    def save_token(self, token_string: str, token_data: TokenMixin):
        raise NotImplementedError()


class InMemoryTokenStorage(TokenStorage):
    def __init__(self):
        self.tokens = {}

    def get_token(self, token_string: str) -> Optional[TokenMixin]:
        return self.tokens.get(token_string)

    def save_token(self, token_string: str, token_data: TokenMixin):
        self.tokens[token_string] = token_data
