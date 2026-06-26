"""
World Bank API Extraction Script

Collects economic context data from the World Bank API.

This script supports:
- GDP per capita analysis
- Unemployment-rate analysis
- Income-group classification
- Regional classification
- Opportunity Score framework
"""

import requests

from scripts.api_client import get_json
from scripts.file_utils import current_date_string, save_raw_json
from scripts.logger import log_start, log_success, log_error, log_complete
from scripts.payload_builder import build_payload


BASE_URL = "https://api.worldbank.org/v2"

INDICATORS = {
    "gdp_per_capita_current_usd": "NY.GDP.PCAP.CD",
    "unemployment_total_percent": "SL.UEM.TOTL.ZS",
}

COUNTRY_ENDPOINT = f"{BASE_URL}/country"
PER_PAGE = 300
DATE_RANGE = "2021:2025"


def fetch_country_metadata():
    """Fetch country metadata, including region and income level."""
    url = COUNTRY_ENDPOINT

    params = {
        "format": "json",
        "per_page": PER_PAGE,
    }

    return get_json(url, params=params)


def fetch_indicator_data(indicator_code):
    """Fetch World Bank indicator time-series data for all countries."""
    url = f"{BASE_URL}/country/all/indicator/{indicator_code}"

    params = {
        "format": "json",
        "per_page": 20000,
        "date": DATE_RANGE,
    }

    return get_json(url, params=params)


def extract_worldbank():
    """Extract World Bank economic context data and save raw JSON archive."""
    log_start("World Bank")

    extracted_data = {}
    errors = []

    try:
        country_metadata = fetch_country_metadata()
        extracted_data["country_metadata"] = country_metadata
        log_success("Country metadata extracted")

    except requests.exceptions.RequestException as error:
        errors.append({
            "source_section": "country_metadata",
            "error": str(error),
        })
        log_error(f"Country metadata failed: {error}")

    for indicator_name, indicator_code in INDICATORS.items():
        try:
            data = fetch_indicator_data(indicator_code)
            extracted_data[indicator_name] = data
            log_success(f"{indicator_name} extracted")

        except requests.exceptions.RequestException as error:
            errors.append({
                "source_section": indicator_name,
                "indicator_code": indicator_code,
                "error": str(error),
            })
            log_error(f"{indicator_name} failed: {error}")

    payload = build_payload(
        source="World Bank",
        data=extracted_data,
        errors=errors,
        metadata={
            "api_type": "World Bank V2 Indicators API",
            "base_url": BASE_URL,
            "date_range": DATE_RANGE,
            "indicators": INDICATORS,
            "sections_extracted": list(extracted_data.keys()),
            "record_count": len(extracted_data),
        },
    )

    filename = f"worldbank_{current_date_string()}.json"
    output_path = save_raw_json(payload, filename)

    log_complete(
        source="World Bank",
        output_path=output_path,
        errors=len(errors),
    )


if __name__ == "__main__":
    extract_worldbank()