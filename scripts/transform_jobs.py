"""
Phase 6 transformation pipeline.

Reads raw JSON archives, normalizes job records from each source, and writes
a standardized processed jobs dataset.
"""

import json
from pathlib import Path

import pandas as pd

from scripts.constants import PROCESSED_DIR, RAW_DIR, STANDARD_JOB_COLUMNS
from scripts.normalizers import normalize_adzuna, normalize_remoteok, normalize_usajobs, normalize_worldbank
from scripts.validators import print_quality_summary, split_valid_invalid_records
from scripts.standardizers import is_data_career_role
from scripts.deduplicator import detect_duplicates, duplicate_summary



OUTPUT_FILE = PROCESSED_DIR / "jobs.csv"
WORLDBANK_OUTPUT_FILE = PROCESSED_DIR / "worldbank.csv"


def load_json_file(file_path: Path) -> dict:
    """Load one raw JSON archive."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_job_id(row_number: int) -> str:
    """Generate stable pipeline job IDs for processed records."""
    return f"JOB-{row_number:06d}"


def find_latest_file(prefix: str) -> Path | None:
    """Find the latest raw file for a given source prefix."""
    files = sorted(RAW_DIR.glob(f"{prefix}*.json"))

    if not files:
        return None

    return files[-1]


def normalize_source(prefix: str, normalizer):
    """Load and normalize the latest raw file for one source."""
    source_file = find_latest_file(prefix)

    if source_file is None:
        print(f"No raw file found for prefix: {prefix}")
        return []

    print(f"Normalizing {source_file}")

    raw_payload = load_json_file(source_file)
    return normalizer(raw_payload, source_file.name)


def transform_worldbank():
    """Normalize World Bank economic context data separately from job postings."""
    source_file = find_latest_file("worldbank_")

    if source_file is None:
        print("No raw World Bank file found.")
        return None

    print(f"Normalizing {source_file}")

    raw_payload = load_json_file(source_file)
    records = normalize_worldbank(raw_payload, source_file.name)

    dataframe = pd.DataFrame(records)
    dataframe.to_csv(WORLDBANK_OUTPUT_FILE, index=False)

    print(f"Processed World Bank data saved to: {WORLDBANK_OUTPUT_FILE}")
    print(f"Total World Bank records: {len(dataframe)}")

    return dataframe


def transform_jobs():
    """Run the Phase 6 job normalization pipeline."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    records = []

    records.extend(normalize_source("remoteok_", normalize_remoteok))
    records.extend(normalize_source("adzuna_", normalize_adzuna))
    records.extend(normalize_source("usajobs_", normalize_usajobs))
    valid_records, invalid_records = split_valid_invalid_records(records)
    dataframe = pd.DataFrame(valid_records, columns=STANDARD_JOB_COLUMNS)
    dataframe = dataframe[
        dataframe.apply(
            lambda row: is_data_career_role(row["job_title"], row["description"]),
            axis=1,
        )
    ].copy()

    if dataframe.empty:
        print("No records were normalized. Check raw data files.")
        return

    dataframe = dataframe.drop(columns=["job_id"], errors="ignore")

    dataframe.insert(
        0,
        "job_id",
        [generate_job_id(index + 1) for index in range(len(dataframe))],
    )

    dataframe = dataframe[STANDARD_JOB_COLUMNS]

    dataframe.to_csv(OUTPUT_FILE, index=False)

    print(f"Processed jobs saved to: {OUTPUT_FILE}")
    print(f"Total normalized records: {len(dataframe)}")
    print_quality_summary(dataframe, invalid_count=len(invalid_records))
    
    summary = duplicate_summary(dataframe)

    print("\nDuplicate Summary")
    print("-----------------")
    print(f"Potential duplicate records: {summary['duplicate_records']}")
    print(f"Duplicate groups: {summary['duplicate_groups']}")

    duplicates = detect_duplicates(dataframe)

    if not duplicates.empty:
        duplicates.to_csv(
            PROCESSED_DIR / "potential_duplicates.csv",
            index=False,
        )

        print(
            f"Potential duplicates saved to: "
            f"{PROCESSED_DIR / 'potential_duplicates.csv'}"
        )


if __name__ == "__main__":
    transform_jobs()
    transform_worldbank()