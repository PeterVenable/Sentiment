import json
import logging
import os


def load_settings(path="settings.json") -> dict:
    """
    Load the configuration settings from a JSON file.
    The file is expected to be in the current working directory.
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logging.error(f"Error loading settings: {e}")
        logging.error(f"cwd: {os.getcwd()}")
        return {}


settings = load_settings()
