"""
Data Loader Module
Loads and summarizes the raw Superstore sales dataset.
"""

import pandas as pd
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw dataset path
RAW_SUPERSTORE_FILE = (
    PROJECT_ROOT / "data" / "raw" / "superstore.csv"
)


def load_raw_sales_data():
    """
    Load the Superstore sales dataset and clean column names.
    """

    # Check whether the file exists
    if not RAW_SUPERSTORE_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_SUPERSTORE_FILE}"
        )

    # Read CSV using semicolon separator
    df = pd.read_csv(
        RAW_SUPERSTORE_FILE,
        sep=";",
        encoding="latin1"
    )

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df


def print_data_summary(df):
    """
    Print a summary of the sales dataset.
    """

    print("=" * 60)
    print("Superstore Sales Dataset Summary")
    print("=" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst rows:")
    print(df.head())


if __name__ == "__main__":
    # Test the data loader
    raw_df = load_raw_sales_data()
    print_data_summary(raw_df)