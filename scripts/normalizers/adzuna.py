"""
Adzuna normalizer.

Converts raw Adzuna API records into the standard Phase 6 jobs schema.
"""

from scripts.cleaners import clean_date, clean_number, clean_text
from scripts.constants import STANDARD_JOB_COLUMNS
from scripts.standardizers import (
    standardize_company,
    standardize_remote_status,
    standardize_salary_currency,
)


def normalize_adzuna(raw_payload, source_file):
    """Normalize Adzuna raw payload into standard job records."""
    records = []

    extraction_date = raw_payload.get("extraction_date")
    raw_pages = raw_payload.get("data", [])
    metadata = raw_payload.get("metadata", {})
    default_country = metadata.get("country")

    for page in raw_pages:
        if not isinstance(page, dict):
            continue

        raw_response = page.get("raw_response", {})
        jobs = raw_response.get("results", [])

        for job in jobs:
            if not isinstance(job, dict):
                continue

            title = clean_text(job.get("title"))
            description = clean_text(job.get("description"))

            if not title:
                continue

            company_data = job.get("company") or {}
            location_data = job.get("location") or {}
            category_data = job.get("category") or {}

            record = {
                "job_id": None,
                "source": "Adzuna",
                "source_job_id": clean_text(job.get("id")),
                "job_title": title,
                "company": standardize_company(company_data.get("display_name")),
                "country": clean_text(default_country),
                "city": clean_text(location_data.get("display_name")),
                "remote_status": standardize_remote_status(
                    job.get("contract_time"),
                    description,
                ),
                "role_category": None,
                "seniority_level": None,
                "salary_min": clean_number(job.get("salary_min")),
                "salary_max": clean_number(job.get("salary_max")),
                "salary_currency": standardize_salary_currency(
                    job.get("salary_currency"),
                    default="GBP",
                ),
                "industry": clean_text(category_data.get("label")),
                "description": description,
                "posted_date": clean_date(job.get("created")),
                "extracted_date": clean_date(extraction_date),
                "source_file": source_file,
            }

            records.append({column: record.get(column) for column in STANDARD_JOB_COLUMNS})

    return records