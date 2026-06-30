"""
Project-wide constants for extraction scripts.
"""

from pathlib import Path

RAW_DIR = Path("data/raw")

DEFAULT_TIMEOUT = 30
REQUEST_DELAY_SECONDS = 1

DATA_CAREER_SEARCH_TERMS = [
    "Data Analyst",
    "Business Intelligence Analyst",
    "BI Analyst",
    "Data Engineer",
    "Analytics Engineer",
    "Data Scientist",
    "Reporting Analyst",
    "Business Analyst",
]

USAJOBS_SEARCH_TERMS = [
    "Data Analyst",
    "Business Intelligence",
    "Data Engineer",
    "Data Scientist",
    "Business Analyst",
]

PROCESSED_DIR = Path("data/processed")

STANDARD_JOB_COLUMNS = [
    "job_id",
    "source",
    "source_job_id",
    "job_title",
    "company",
    "country",
    "city",
    "remote_status",
    "role_category",
    "seniority_level",
    "salary_min",
    "salary_max",
    "salary_currency",
    "industry",
    "description",
    "posted_date",
    "extracted_date",
    "source_file",
]