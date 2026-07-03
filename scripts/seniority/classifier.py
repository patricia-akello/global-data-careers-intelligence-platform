"""
Reusable seniority classification logic.

This module classifies job postings into standardized seniority levels
using job titles, descriptions, and experience signals.
"""

import re
from scripts.seniority.taxonomy import SENIORITY_KEYWORDS, SENIORITY_PRIORITY


def normalize_text(*values):
    """
    Combine text fields into one lowercase searchable string.
    Missing values are ignored.
    """
    cleaned_values = []

    for value in values:
        if value is None:
            continue

        text = str(value).strip().lower()

        if text:
            cleaned_values.append(text)

    return " ".join(cleaned_values)


def extract_years_experience(text):
    """
    Extract numeric years of experience from job text.
    Returns the highest detected year value.
    """
    if not text:
        return None

    patterns = [
        r"(\d+)\+?\s*years",
        r"(\d+)\+?\s*yrs",
        r"(\d+)\s*-\s*(\d+)\s*years",
        r"(\d+)\s*to\s*(\d+)\s*years",
    ]

    years_found = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            if isinstance(match, tuple):
                years_found.extend([int(value) for value in match if value])
            else:
                years_found.append(int(match))

    if not years_found:
        return None

    return max(years_found)


def classify_by_experience(years):
    """
    Map extracted years of experience to seniority levels.
    """
    if years is None:
        return None

    if years <= 1:
        return "Entry Level"

    if years <= 2:
        return "Junior"

    if years <= 4:
        return "Mid Level"

    if years <= 7:
        return "Senior"

    if years <= 9:
        return "Lead"

    return "Principal"


def classify_by_keywords(text):
    """
    Classify seniority using keyword rules and priority order.
    """
    for seniority_level in SENIORITY_PRIORITY:
        if seniority_level == "Unknown":
            continue

        keywords = SENIORITY_KEYWORDS.get(seniority_level, [])

        for keyword in keywords:
            if keyword in text:
                return seniority_level

    return None


def classify_seniority(job_title=None, description=None):
    """
    Classify a job posting into one standardized seniority level.
    """
    text = normalize_text(job_title, description)

    if not text:
        return "Unknown"

    keyword_result = classify_by_keywords(text)
    experience_years = extract_years_experience(text)
    experience_result = classify_by_experience(experience_years)

    if keyword_result and experience_result:
        keyword_priority = SENIORITY_PRIORITY.index(keyword_result)
        experience_priority = SENIORITY_PRIORITY.index(experience_result)

        return (
            keyword_result
            if keyword_priority < experience_priority
            else experience_result
        )

    if keyword_result:
        return keyword_result

    if experience_result:
        return experience_result

    return "Unknown"