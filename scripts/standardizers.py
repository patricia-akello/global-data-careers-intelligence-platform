"""
Standardization helpers for normalized job records.
"""

from scripts.cleaners import clean_text


def standardize_remote_status(value, description=None):
    """Standardize remote status values."""
    combined = " ".join(
        text for text in [clean_text(value), clean_text(description)] if text
    ).lower()

    if not combined:
        return "Unknown"

    remote_terms = [
        "remote",
        "work from anywhere",
        "work-from-anywhere",
        "distributed",
        "home based",
        "home-based",
    ]

    hybrid_terms = ["hybrid", "part remote", "partly remote"]

    if any(term in combined for term in remote_terms):
        return "Remote"

    if any(term in combined for term in hybrid_terms):
        return "Hybrid"

    return "On-site"


def standardize_salary_currency(value, default="Unknown"):
    """Standardize salary currency."""
    text = clean_text(value)

    if not text:
        return default

    return text.upper()


def standardize_company(value):
    """Basic company name standardization."""
    text = clean_text(value)

    if not text:
        return None

    replacements = {
        "Microsoft Corporation": "Microsoft",
        "MSFT": "Microsoft",
        "Amazon Web Services": "AWS",
        "Google LLC": "Google",
    }

    return replacements.get(text, text)


def is_data_career_role(title, description=None):
    """Return True if the job appears relevant to the project scope."""
    combined = " ".join(
        text for text in [clean_text(title), clean_text(description)] if text
    ).lower()

    include_terms = [
        "data analyst",
        "business intelligence",
        "bi analyst",
        "data engineer",
        "analytics engineer",
        "data scientist",
        "reporting analyst",
        "business analyst",
    ]

    exclude_terms = [
        "marketing analyst",
        "financial analyst",
        "cybersecurity analyst",
        "healthcare analyst",
        "scheduling coordinator",
        "marketing manager",
        "travel coordinator",
    ]

    if any(term in combined for term in exclude_terms):
        return False

    return any(term in combined for term in include_terms)