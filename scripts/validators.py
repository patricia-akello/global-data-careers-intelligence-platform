"""
Validation helpers for Phase 6 processed job records.
"""

REQUIRED_FIELDS = ["job_title", "source", "source_file"]


def is_valid_job_record(record):
    """Return True if a normalized job record has required fields."""
    return all(record.get(field) not in [None, ""] for field in REQUIRED_FIELDS)


def split_valid_invalid_records(records):
    """Separate valid and invalid normalized records."""
    valid_records = []
    invalid_records = []

    for record in records:
        if is_valid_job_record(record):
            valid_records.append(record)
        else:
            invalid_records.append(record)

    return valid_records, invalid_records


def print_quality_summary(dataframe, invalid_count=0):
    """Print basic quality checks for the processed jobs dataset."""
    print("\nPhase 6 Quality Summary")
    print("-----------------------")
    print(f"Valid records: {len(dataframe)}")
    print(f"Invalid records skipped: {invalid_count}")

    if dataframe.empty:
        return

    print("\nRecords by source:")
    print(dataframe["source"].value_counts(dropna=False).to_string())

    print("\nMissing values:")
    print(f"Missing salary_min: {dataframe['salary_min'].isna().sum()}")
    print(f"Missing salary_max: {dataframe['salary_max'].isna().sum()}")
    print(f"Missing country: {dataframe['country'].isna().sum()}")
    print(f"Missing city: {dataframe['city'].isna().sum()}")
    print(f"Missing description: {dataframe['description'].isna().sum()}")