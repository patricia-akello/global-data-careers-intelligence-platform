"""
World Bank normalizer.

Converts raw World Bank API responses into a processed economic context dataset.
"""

from scripts.cleaners import clean_number, clean_text


def _latest_country_values(indicator_rows):
    """Return latest non-null value per country from World Bank indicator rows."""
    latest_values = {}

    for row in indicator_rows:
        if not isinstance(row, dict):
            continue

        country = row.get("country") or {}
        country_code = clean_text(country.get("id"))
        value = clean_number(row.get("value"))
        year = clean_text(row.get("date"))

        if not country_code or value is None:
            continue

        existing = latest_values.get(country_code)

        if existing is None or year > existing["year"]:
            latest_values[country_code] = {
                "year": year,
                "value": value,
            }

    return latest_values


def normalize_worldbank(raw_payload, source_file):
    """Normalize World Bank economic context data."""
    data = raw_payload.get("data", {})
    extraction_date = raw_payload.get("extraction_date")

    country_metadata = data.get("country_metadata", [])
    gdp_raw = data.get("gdp_per_capita_current_usd", [])
    unemployment_raw = data.get("unemployment_total_percent", [])

    countries = country_metadata[1] if len(country_metadata) > 1 else []
    gdp_rows = gdp_raw[1] if len(gdp_raw) > 1 else []
    unemployment_rows = unemployment_raw[1] if len(unemployment_raw) > 1 else []

    latest_gdp = _latest_country_values(gdp_rows)
    latest_unemployment = _latest_country_values(unemployment_rows)

    records = []

    for country in countries:
        if not isinstance(country, dict):
            continue

        country_code = clean_text(country.get("id"))

        if not country_code:
            continue

        region = country.get("region") or {}
        income_level = country.get("incomeLevel") or {}

        records.append({
            "country_code": country_code,
            "country": clean_text(country.get("name")),
            "region": clean_text(region.get("value")),
            "income_group": clean_text(income_level.get("value")),
            "gdp_per_capita": latest_gdp.get(country_code, {}).get("value"),
            "gdp_year": latest_gdp.get(country_code, {}).get("year"),
            "unemployment_rate": latest_unemployment.get(country_code, {}).get("value"),
            "unemployment_year": latest_unemployment.get(country_code, {}).get("year"),
            "extracted_date": extraction_date,
            "source_file": source_file,
        })

    return records