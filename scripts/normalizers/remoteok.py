"""
RemoteOK normalizer.

Converts raw RemoteOK API records into the standard Phase 6 jobs schema.
"""

from scripts.cleaners import clean_date, clean_number, clean_text
from scripts.constants import STANDARD_JOB_COLUMNS
from scripts.standardizers import (
    standardize_company,
    standardize_remote_status,
    standardize_salary_currency,
)


def normalize_remoteok(raw_payload, source_file):
    """Normalize RemoteOK raw payload into standard job records."""
    records = []

    extraction_date = raw_payload.get("extraction_date")
    raw_data = raw_payload.get("data", [])

    for item in raw_data:
        if not isinstance(item, dict):
            continue

        title = clean_text(item.get("position"))
        company = standardize_company(item.get("company"))
        description = clean_text(item.get("description"))

        if not title:
            continue

        record = {
            "job_id": None,
            "source": "RemoteOK",
            "source_job_id": clean_text(item.get("id")),
            "job_title": title,
            "company": company,
            "country": clean_text(item.get("location")),
            "city": None,
            "remote_status": standardize_remote_status("remote", description),
            "role_category": None,
            "seniority_level": None,
            "salary_min": clean_number(item.get("salary_min")),
            "salary_max": clean_number(item.get("salary_max")),
            "salary_currency": standardize_salary_currency(
                item.get("salary_currency"),
                default="Unknown",
            ),
            "industry": None,
            "description": description,
            "posted_date": clean_date(item.get("date")),
            "extracted_date": clean_date(extraction_date),
            "source_file": source_file,
        }

        records.append({column: record.get(column) for column in STANDARD_JOB_COLUMNS})

    return records