"""
RemoteOK API Extraction Script

Purpose:
Collect remote technology job postings from the RemoteOK API.

This script supports later phases:
- Remote hiring analysis
- Geography analysis
- Role classification
- Skill extraction
- Raw JSON archiving
"""

import json
from datetime import datetime
from pathlib import Path

import requests


API_URL = "https://remoteok.com/api"
RAW_DIR = Path("data/raw")


def fetch_remoteok_jobs():
    """Fetch raw job postings from RemoteOK."""
    headers = {
        "User-Agent": "global-data-careers-intelligence-platform"
    }

    response = requests.get(API_URL, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_remoteok_jobs():
    """Extract RemoteOK jobs and save the raw API archive."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y_%m_%d")
    output_file = RAW_DIR / f"remoteok_{today}.json"

    errors = []
    data = []

    try:
        data = fetch_remoteok_jobs()
        print(f"RemoteOK records extracted: {len(data)}")

    except requests.exceptions.RequestException as error:
        errors.append({
            "error": str(error),
            "error_time": datetime.now().isoformat(),
        })

        print(f"RemoteOK extraction failed: {error}")

    payload = {
        "source": "RemoteOK",
        "extraction_date": datetime.now().isoformat(),
        "record_count": len(data),
        "total_errors": len(errors),
        "errors": errors,
        "data": data,
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4, ensure_ascii=False)

    print(f"RemoteOK extraction completed: {output_file}")
    print(f"Errors: {len(errors)}")


if __name__ == "__main__":
    extract_remoteok_jobs()