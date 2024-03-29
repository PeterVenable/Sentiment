import logging

from authlib.integrations.flask_oauth2 import ResourceProtector

from .storage import InMemoryTokenStorage, TokenStorage
from .token import Token
from .validator import Validator


def store_tokens_from_settings(storage: TokenStorage):
    from settings import settings
    tokens = settings.get("tokens", [])
    if not tokens:
        return
    if not isinstance(tokens, list):
        raise ValueError("tokens must be a list of dictionaries")
    for token in tokens:
        if not isinstance(token, dict):
            raise ValueError("tokens must be a list of dictionaries")
        client_id = token.get("client_id")
        if not (client_id and isinstance(client_id, str)):
            raise ValueError("client_id must be a string")
        access_token = token.get("access_token", "")
        if not isinstance(access_token, str):
            raise ValueError("access_token must be a string")
        storage.save_token(client_id, Token(client_id, access_token))


def get_resource_protector():
    storage = InMemoryTokenStorage()
    store_tokens_from_settings(storage)
    require_oauth = ResourceProtector()
    require_oauth.register_token_validator(Validator(storage))
    return require_oauth
