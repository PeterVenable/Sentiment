import json
import logging


def load_settings(path="settings.json") -> dict:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logging.error(f"Error loading settings: {e}")
        return {}


settings = load_settings()
