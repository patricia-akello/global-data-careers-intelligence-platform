"""
Centralized environment configuration.

This file loads API credentials from .env.
Secrets are never written directly inside extraction scripts.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "gb")

USAJOBS_EMAIL = os.getenv("USAJOBS_EMAIL")
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")


def require_env_value(value, name):
    """Raise a clear error when a required environment variable is missing."""
    if not value:
        raise ValueError(f"Missing {name}. Add it to your .env file.")