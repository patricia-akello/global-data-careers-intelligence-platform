"""
USAJobs API Extraction Script

Purpose:
Collect structured government job postings from the USAJobs Search API.

This script supports later phases:
- Role classification
- Seniority classification
- Skill extraction
- Salary analysis
- Metadata standardization

Security:
API credentials are loaded from the local .env file and are not committed to GitHub.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


# Load secrets from .env
load_dotenv()

USAJOBS_EMAIL = os.getenv("USAJOBS_EMAIL")
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")

RAW_DIR = Path("data/raw")

SEARCH_TERMS = [
    "Data Analyst",
    "Business Intelligence",
    "Data Engineer",
    "Data Scientist",
    "Business Analyst",
]

RESULTS_PER_PAGE = 25
MAX_PAGES_PER_TERM = 2
REQUEST_DELAY_SECONDS = 1


def validate_credentials():
    """Stop the script early if USAJobs credentials are missing."""
    if not USAJOBS_EMAIL or not USAJOBS_API_KEY:
        raise ValueError(
            "Missing USAJOBS_EMAIL or USAJOBS_API_KEY. Add them to your .env file."
        )


def build_headers():
    """Build the required USAJobs authentication headers."""
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

    response = requests.get(
        url,
        headers=build_headers(),
        params=params,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def extract_usajobs():
    """Extract USAJobs data and save raw JSON archive."""
    validate_credentials()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y_%m_%d")
    output_file = RAW_DIR / f"usajobs_{today}.json"

    extracted_pages = []
    errors = []

    for search_term in SEARCH_TERMS:
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

                print(f"  Page {page}: {len(items)} records")

                time.sleep(REQUEST_DELAY_SECONDS)

            except requests.exceptions.RequestException as error:
                errors.append({
                    "search_term": search_term,
                    "page": page,
                    "error": str(error),
                    "error_time": datetime.now().isoformat(),
                })

                print(f"  Error on page {page}: {error}")

    payload = {
        "source": "USAJobs",
        "extraction_date": datetime.now().isoformat(),
        "search_terms": SEARCH_TERMS,
        "results_per_page": RESULTS_PER_PAGE,
        "max_pages_per_term": MAX_PAGES_PER_TERM,
        "successful_pages": len(extracted_pages),
        "total_errors": len(errors),
        "errors": errors,
        "data": extracted_pages,
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4, ensure_ascii=False)

    print(f"USAJobs extraction completed: {output_file}")
    print(f"Successful pages: {len(extracted_pages)}")
    print(f"Errors: {len(errors)}")


if __name__ == "__main__":
    extract_usajobs()