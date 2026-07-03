"""
Phase 8 Seniority Classification Pipeline.

Loads the processed jobs dataset, assigns seniority_level,
and writes the enriched dataset back to data/processed/jobs.csv.
"""

from pathlib import Path
import pandas as pd

from scripts.seniority.classifier import classify_seniority


PROJECT_ROOT = Path(__file__).resolve().parents[1]
JOBS_PATH = PROJECT_ROOT / "data" / "processed" / "jobs.csv"


def run_seniority_classification():
    """
    Apply seniority classification to the processed jobs dataset.
    """
    if not JOBS_PATH.exists():
        raise FileNotFoundError(f"Could not find processed jobs file: {JOBS_PATH}")

    jobs = pd.read_csv(JOBS_PATH)

    required_columns = ["job_title", "description"]

    for column in required_columns:
        if column not in jobs.columns:
            raise ValueError(f"Missing required column: {column}")

    jobs["seniority_level"] = jobs.apply(
        lambda row: classify_seniority(
            job_title=row.get("job_title"),
            description=row.get("description"),
        ),
        axis=1,
    )

    jobs.to_csv(JOBS_PATH, index=False)

    print("Seniority classification completed.")
    print(f"Updated file: {JOBS_PATH}")
    print("\nSeniority distribution:")
    print(jobs["seniority_level"].value_counts(dropna=False))


if __name__ == "__main__":
    run_seniority_classification()