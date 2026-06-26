"""
File utility functions for extraction scripts.
"""

import json
from datetime import datetime

from scripts.constants import RAW_DIR


def current_date_string():
    """Return today's date as YYYY_MM_DD."""
    return datetime.now().strftime("%Y_%m_%d")


def current_timestamp():
    """Return the current timestamp in ISO format."""
    return datetime.now().isoformat()


def save_raw_json(payload, filename):
    """Save a payload as formatted JSON inside data/raw."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    output_path = RAW_DIR / filename

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4, ensure_ascii=False)

    return output_path