"""
Phase 7 - Role Classification Pipeline

Reads the standardized jobs dataset, classifies each job into
one of the project's role categories, and saves the updated dataset.
"""

from pathlib import Path

import pandas as pd

from scripts.classification.classifier import classify_role


DATA_DIR = Path("data/processed")
INPUT_FILE = DATA_DIR / "jobs.csv"
OUTPUT_FILE = DATA_DIR / "jobs.csv"


def load_jobs():
    """
    Load the processed jobs dataset.
    """
    return pd.read_csv(INPUT_FILE)


def classify_jobs(df):
    """
    Add the role_category column.
    """

    df["role_category"] = df.apply(
        lambda row: classify_role(
            row.get("job_title"),
            row.get("description"),
        ),
        axis=1,
    )

    return df


def print_summary(df):
    """
    Print classification statistics.
    """

    print("\nRole Classification Summary")
    print("-" * 40)

    summary = (
        df["role_category"]
        .value_counts()
        .sort_index()
    )

    for role, count in summary.items():
        print(f"{role:<25} {count:>6}")

    print("-" * 40)
    print(f"Total Jobs{'':<15}{len(df):>6}")


def save_jobs(df):
    """
    Save the updated dataset.
    """
    df.to_csv(OUTPUT_FILE, index=False)


def main():

    print("Loading processed dataset...")

    jobs = load_jobs()

    print(f"Loaded {len(jobs)} jobs.")

    jobs = classify_jobs(jobs)

    save_jobs(jobs)

    print_summary(jobs)

    print("\nUpdated dataset saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()