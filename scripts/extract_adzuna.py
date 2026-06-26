"""
Adzuna API Extraction Script

Collects job posting data from Adzuna and saves raw API responses
using shared project utilities.
"""

import time

import requests

from scripts.api_client import get_json
from scripts.config import ADZUNA_APP_ID, ADZUNA_APP_KEY, ADZUNA_COUNTRY, require_env_value
from scripts.constants import DATA_CAREER_SEARCH_TERMS, REQUEST_DELAY_SECONDS
from scripts.file_utils import current_timestamp, current_date_string, save_raw_json
from scripts.logger import log_start, log_success, log_error, log_complete


MAX_PAGES_PER_TERM = 2
RESULTS_PER_PAGE = 50


def validate_credentials():
    """Stop the script if Adzuna credentials are missing."""
    require_env_value(ADZUNA_APP_ID, "ADZUNA_APP_ID")
    require_env_value(ADZUNA_APP_KEY, "ADZUNA_APP_KEY")


def fetch_adzuna_page(search_term, page):
    """Fetch one page of Adzuna job results."""
    url = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": search_term,
        "results_per_page": RESULTS_PER_PAGE,
        "content-type": "application/json",
    }

    return get_json(url, params=params)


def extract_adzuna_jobs():
    """Extract Adzuna jobs and save a raw JSON archive."""
    validate_credentials()
    log_start("Adzuna")

    extracted_pages = []
    errors = []

    for search_term in DATA_CAREER_SEARCH_TERMS:
        print(f"Extracting: {search_term}")

        for page in range(1, MAX_PAGES_PER_TERM + 1):
            try:
                data = fetch_adzuna_page(search_term, page)
                jobs = data.get("results", [])

                extracted_pages.append({
                    "search_term": search_term,
                    "page": page,
                    "records_returned": len(jobs),
                    "raw_response": data,
                })

                log_success(f"Page {page}: {len(jobs)} records")
                time.sleep(REQUEST_DELAY_SECONDS)

            except requests.exceptions.RequestException as error:
                errors.append({
                    "search_term": search_term,
                    "page": page,
                    "error": str(error),
                    "error_time": current_timestamp(),
                })

                log_error(f"{search_term}, page {page}: {error}")

    payload = {
        "source": "Adzuna",
        "country": ADZUNA_COUNTRY,
        "extraction_date": current_timestamp(),
        "search_terms": DATA_CAREER_SEARCH_TERMS,
        "max_pages_per_term": MAX_PAGES_PER_TERM,
        "results_per_page": RESULTS_PER_PAGE,
        "successful_pages": len(extracted_pages),
        "total_errors": len(errors),
        "errors": errors,
        "data": extracted_pages,
    }

    filename = f"adzuna_{ADZUNA_COUNTRY}_{current_date_string()}.json"
    output_path = save_raw_json(payload, filename)

    log_complete(
        source="Adzuna",
        output_path=output_path,
        successful_pages=len(extracted_pages),
        errors=len(errors),
    )


if __name__ == "__main__":
    extract_adzuna_jobs()