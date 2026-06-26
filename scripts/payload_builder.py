"""
Payload builder for raw extraction archives.

This creates a consistent JSON structure across all API sources.
"""

from scripts.file_utils import current_timestamp


PIPELINE_VERSION = "1.0"


def build_payload(source, data, errors, metadata=None):
    """
    Build a standardized raw extraction payload.

    Args:
        source: Name of the API/source.
        data: Extracted raw data or extracted pages.
        errors: List of extraction errors.
        metadata: Optional dictionary of source-specific metadata.

    Returns:
        Dictionary ready to be saved as JSON.
    """
    if metadata is None:
        metadata = {}

    return {
        "source": source,
        "pipeline_version": PIPELINE_VERSION,
        "extraction_date": current_timestamp(),
        "record_count": metadata.get("record_count"),
        "successful_pages": metadata.get("successful_pages"),
        "total_errors": len(errors),
        "metadata": metadata,
        "errors": errors,
        "data": data,
    }