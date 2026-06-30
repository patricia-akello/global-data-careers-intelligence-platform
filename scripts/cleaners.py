"""
Reusable cleaning helpers for Phase 6 transformation.
"""

from datetime import datetime
from typing import Any


def clean_text(value: Any) -> str | None:
    """Return stripped text or None."""
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    return " ".join(text.split())


def clean_number(value: Any) -> float | None:
    """Convert a value to float when possible."""
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_date(value: Any) -> str | None:
    """Return date-like values as ISO strings when possible."""
    if value is None or value == "":
        return None

    text = str(value).strip()

    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return text[:10] if len(text) >= 10 else text