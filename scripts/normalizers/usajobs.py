"""
USAJobs normalizer.

Converts raw USAJobs API records into the standard Phase 6 jobs schema.
"""

from scripts.cleaners import clean_date, clean_number, clean_text
from scripts.constants import STANDARD_JOB_COLUMNS
from scripts.standardizers import standardize_remote_status


def _extract_location(position_location):
    """Extract city and country from USAJobs PositionLocation."""
    if not position_location:
        return None, None

    first_location = position_location[0]

    if not isinstance(first_location, dict):
        return None, None

    city = clean_text(first_location.get("LocationName"))
    country = clean_text(first_location.get("CountryCode"))

    return city, country


def normalize_usajobs(raw_payload, source_file):
    """Normalize USAJobs raw payload into standard job records."""
    records = []

    extraction_date = raw_payload.get("extraction_date")
    raw_pages = raw_payload.get("data", [])

    for page in raw_pages:
        if not isinstance(page, dict):
            continue

        raw_response = page.get("raw_response", {})
        search_result = raw_response.get("SearchResult", {})
        items = search_result.get("SearchResultItems", [])

        for item in items:
            if not isinstance(item, dict):
                continue

            descriptor = item.get("MatchedObjectDescriptor", {})
            if not isinstance(descriptor, dict):
                continue

            title = clean_text(descriptor.get("PositionTitle"))
            description = clean_text(descriptor.get("UserArea", {}).get("Details", {}).get("JobSummary"))

            if not title:
                continue

            city, country = _extract_location(descriptor.get("PositionLocation"))

            salary_data = descriptor.get("PositionRemuneration") or []
            salary_min = None
            salary_max = None
            salary_currency = "USD"

            if salary_data and isinstance(salary_data[0], dict):
                salary_min = clean_number(salary_data[0].get("MinimumRange"))
                salary_max = clean_number(salary_data[0].get("MaximumRange"))
                salary_currency = clean_text(salary_data[0].get("CurrencyCode")) or "USD"

            record = {
                "job_id": None,
                "source": "USAJobs",
                "source_job_id": clean_text(descriptor.get("PositionID")),
                "job_title": title,
                "company": clean_text(descriptor.get("OrganizationName")),
                "country": country,
                "city": city,
                "remote_status": standardize_remote_status(
                    descriptor.get("PositionLocationDisplay"),
                    description,
                ),
                "role_category": None,
                "seniority_level": None,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_currency": salary_currency,
                "industry": "Government",
                "description": description,
                "posted_date": clean_date(descriptor.get("PublicationStartDate")),
                "extracted_date": clean_date(extraction_date),
                "source_file": source_file,
            }

            records.append({column: record.get(column) for column in STANDARD_JOB_COLUMNS})

    return records