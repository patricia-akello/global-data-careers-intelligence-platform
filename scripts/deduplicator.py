"""
Duplicate detection utilities for processed job records.
"""

import pandas as pd


DUPLICATE_KEYS = [
    "job_title",
    "company",
    "country",
]


def detect_duplicates(dataframe: pd.DataFrame):
    """
    Return potential duplicate job postings.

    Records are considered duplicates when they share the same
    job title, company, and country.
    """

    duplicate_mask = dataframe.duplicated(
        subset=DUPLICATE_KEYS,
        keep=False,
    )

    duplicates = dataframe.loc[duplicate_mask].copy()

    return duplicates.sort_values(DUPLICATE_KEYS)


def duplicate_summary(dataframe: pd.DataFrame):
    """
    Return duplicate statistics.
    """

    duplicates = detect_duplicates(dataframe)

    return {
        "duplicate_records": len(duplicates),
        "duplicate_groups": (
            duplicates.groupby(DUPLICATE_KEYS)
            .ngroups
            if not duplicates.empty
            else 0
        ),
    }