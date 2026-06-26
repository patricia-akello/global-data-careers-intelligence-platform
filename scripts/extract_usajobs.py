"""
USAJobs API Extraction Script

Collects structured government job postings from the USAJobs Search API
and saves raw API responses using shared project utilities.
"""

import time

import requests

from scripts.api_client import get_json
from scripts.config import USAJOBS_EMAIL, USAJOBS_API_KEY, require_env_value
from scripts.constants import USAJOBS_SEARCH_TERMS, REQUEST_DELAY_SECONDS
from scripts.file_utils import current_timestamp, current_date_string, save_raw_json
from scripts.logger import log_start, log_success, log_error, log_complete


RESULTS_PER_PAGE = 25
MAX_PAGES_PER_TERM = 2


def validate_credentials():
    """Stop the script if USAJobs credentials are missing."""
    require_env_value(USAJOBS_EMAIL, "USAJOBS_EMAIL")
    require_env_value(USAJOBS_API_KEY, "USAJOBS_API_KEY")


def build_headers():
    """Build required USAJobs authentication headers."""
    return {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_EMAIL,
        "Authorization-Key": USAJOBS_API_KEY,
    }


def fetch_usajobs_page(search_term, page):
    """Fetch one page of USAJobs search results."""
    url = "https://data.usajobs.gov/api/Search"

    params = {
        "Keyword": search_term,
        "ResultsPerPage": RESULTS_PER_PAGE,
        "Page": page,
        "Fields": "Full",
        "WhoMayApply": "public",
        "SortField": "opendate",
        "SortDirection": "desc",
    }

    return get_json(
        url=url,
        headers=build_headers(),
        params=params,
    )


def extract_usajobs():
    """Extract USAJobs data and save a raw JSON archive."""
    validate_credentials()
    log_start("USAJobs")

    extracted_pages = []
    errors = []

    for search_term in USAJOBS_SEARCH_TERMS:
        print(f"Extracting: {search_term}")

        for page in range(1, MAX_PAGES_PER_TERM + 1):
            try:
                data = fetch_usajobs_page(search_term, page)

                search_result = data.get("SearchResult", {})
                items = search_result.get("SearchResultItems", [])

                extracted_pages.append({
                    "search_term": search_term,
                    "page": page,
                    "records_returned": len(items),
                    "total_matching_records": search_result.get("SearchResultCountAll"),
                    "raw_response": data,
                })

                log_success(f"Page {page}: {len(items)} records")
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
        "source": "USAJobs",
        "extraction_date": current_timestamp(),
        "search_terms": USAJOBS_SEARCH_TERMS,
        "results_per_page": RESULTS_PER_PAGE,
        "max_pages_per_term": MAX_PAGES_PER_TERM,
        "successful_pages": len(extracted_pages),
        "total_errors": len(errors),
        "errors": errors,
        "data": extracted_pages,
    }

    filename = f"usajobs_{current_date_string()}.json"
    output_path = save_raw_json(payload, filename)

    log_complete(
        source="USAJobs",
        output_path=output_path,
        successful_pages=len(extracted_pages),
        errors=len(errors),
    )


if __name__ == "__main__":
    extract_usajobs()