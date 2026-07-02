"""
Role classification engine.

Uses both job titles and job descriptions to assign each job
to one standardized role category.
"""

from scripts.classification.taxonomy import (
    ROLE_PRIORITY,
    ROLE_KEYWORDS,
)


def normalize_text(*values):
    """
    Combine text fields into one searchable string.
    """
    return " ".join(
        str(value).lower()
        for value in values
        if value is not None
    )


def classify_role(job_title, description):
    """
    Classify a job into one standardized role category.

    Parameters
    ----------
    job_title : str
    description : str

    Returns
    -------
    str
        One of:
        - Analytics Engineer
        - Data Engineer
        - Data Scientist
        - BI Analyst
        - Data Analyst
        - Other Data Role
    """

    text = normalize_text(job_title, description)

    for role in ROLE_PRIORITY:
        keywords = ROLE_KEYWORDS[role]

        if any(keyword in text for keyword in keywords):
            return role

    return "Other Data Role"