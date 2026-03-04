"""
Configuration for HamAlert Client

User-specific settings are loaded from ~/.hamalert/config.json.
Copy the example below to that path and fill in your values:

{
    "host": "hamalert.org",
    "port": 7300,
    "callsign": "YOURCALL",
    "password": "yourpassword",
    "timeout": 30,
    "mode": "FT8"
}

Available modes (comma-separate multiple values, e.g. "FT8,FT4"):
  CW, SSB, AM, FM, RTTY, PSK31, PSK63, FT8, FT4, JT65, JT9, WSPR, MSK144, Q65, JS8, FST4, FST4W, OLIVIA, MFSK
"""

import json
import os

# Defaults — overridden by the user config file
DEFAULT_CONFIG = {
    "host": "hamalert.org",
    "port": 7300,
    "callsign": None,
    "password": None,
    "timeout": 30,
    # Available modes: CW, SSB, AM, FM, RTTY, PSK31, PSK63, FT8, FT4, JT65, JT9, WSPR, MSK144, Q65, JS8, FST4, FST4W, OLIVIA, MFSK
    "mode": "FT8",
}

USER_CONFIG_PATH = os.path.expanduser("~/.hamalert/config.json")


def load_config():
    """
    Load configuration, merging defaults with the user config file.

    Returns:
        dict: Merged configuration dictionary.

    Raises:
        FileNotFoundError: If the user config file does not exist.
        ValueError: If required fields (callsign, password) are missing.
    """
    config = dict(DEFAULT_CONFIG)

    if not os.path.exists(USER_CONFIG_PATH):
        raise FileNotFoundError(
            f"User config file not found: {USER_CONFIG_PATH}\n"
            "Create it with at least {\"callsign\": \"YOURCALL\", \"password\": \"yourpassword\"}"
        )

    with open(USER_CONFIG_PATH, "r") as f:
        user_config = json.load(f)

    config.update(user_config)

    missing = [k for k in ("callsign", "password") if not config.get(k)]
    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(missing)}")

    return config
