"""
Reusable API client helper.
"""

import requests

from scripts.constants import DEFAULT_TIMEOUT


def get_json(url, headers=None, params=None, timeout=DEFAULT_TIMEOUT):
    """Send a GET request and return JSON data."""
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=timeout,
    )

    response.raise_for_status()
    return response.json()