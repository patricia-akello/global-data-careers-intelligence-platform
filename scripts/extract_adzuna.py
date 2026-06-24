"""
Extract raw job posting data from the Adzuna API.

This script:
1. Reads API credentials from .env
2. Searches selected data-career roles
3. Extracts multiple pages per role
4. Saves raw JSON responses to data/raw/
5. Records metadata and errors for auditability
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
COUNTRY = os.getenv("ADZUNA_COUNTRY", "gb")

RAW_DIR = Path("data/raw")

SEARCH_TERMS = [
    "Data Analyst",
    "Business Intelligence Analyst",
    "BI Analyst",
    "Data Engineer",
    "Analytics Engineer",
    "Data Scientist",
    "Reporting Analyst",
    "Business Analyst",
]

MAX_PAGES_PER_TERM = 2
RESULTS_PER_PAGE = 50
REQUEST_DELAY_SECONDS = 1


def validate_credentials():
    """Stop the script if Adzuna credentials are missing."""
    if not APP_ID or not APP_KEY:
        raise ValueError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env file.")


def fetch_page(search_term, page):
    """Fetch one page of Adzuna job results."""
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": search_term,
        "results_per_page": RESULTS_PER_PAGE,
        "content-type": "application/json",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_adzuna_jobs():
    """Extract Adzuna jobs and save the raw API archive."""
    validate_credentials()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y_%m_%d")
    output_path = RAW_DIR / f"adzuna_{COUNTRY}_{today}.json"

    extracted_pages = []
    errors = []

    for search_term in SEARCH_TERMS:
        print(f"Extracting: {search_term}")

        for page in range(1, MAX_PAGES_PER_TERM + 1):
            try:
                data = fetch_page(search_term, page)
                jobs = data.get("results", [])

                extracted_pages.append({
                    "search_term": search_term,
                    "page": page,
                    "records_returned": len(jobs),
                    "raw_response": data,
                })

                print(f"  Page {page}: {len(jobs)} records")

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
        "source": "Adzuna",
        "country": COUNTRY,
        "extraction_date": datetime.now().isoformat(),
        "search_terms": SEARCH_TERMS,
        "max_pages_per_term": MAX_PAGES_PER_TERM,
        "results_per_page": RESULTS_PER_PAGE,
        "successful_pages": len(extracted_pages),
        "total_errors": len(errors),
        "errors": errors,
        "data": extracted_pages,
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4, ensure_ascii=False)

    print(f"Adzuna extraction completed: {output_path}")
    print(f"Successful pages: {len(extracted_pages)}")
    print(f"Errors: {len(errors)}")


if __name__ == "__main__":
    extract_adzuna_jobs()