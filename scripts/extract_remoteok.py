"""
RemoteOK API Extraction Script

Collects remote technology job postings from RemoteOK and saves
the raw API response using shared project utilities.
"""

import requests

from scripts.api_client import get_json
from scripts.file_utils import current_timestamp, current_date_string, save_raw_json
from scripts.logger import log_start, log_success, log_error, log_complete


API_URL = "https://remoteok.com/api"


def fetch_remoteok_jobs():
    """Fetch raw job postings from RemoteOK."""
    headers = {
        "User-Agent": "global-data-careers-intelligence-platform"
    }

    return get_json(API_URL, headers=headers)


def extract_remoteok_jobs():
    """Extract RemoteOK jobs and save a raw JSON archive."""
    log_start("RemoteOK")

    errors = []
    data = []

    try:
        data = fetch_remoteok_jobs()
        log_success(f"Records extracted: {len(data)}")

    except requests.exceptions.RequestException as error:
        errors.append({
            "error": str(error),
            "error_time": current_timestamp(),
        })

        log_error(str(error))

    payload = {
        "source": "RemoteOK",
        "extraction_date": current_timestamp(),
        "record_count": len(data),
        "total_errors": len(errors),
        "errors": errors,
        "data": data,
    }

    filename = f"remoteok_{current_date_string()}.json"
    output_path = save_raw_json(payload, filename)

    log_complete(
        source="RemoteOK",
        output_path=output_path,
        errors=len(errors),
    )


if __name__ == "__main__":
    extract_remoteok_jobs()