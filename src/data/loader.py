from pathlib import Path

import pandas as pd


def get_csv_files(data_folder):
    """
    Return all CSV files from a dataset folder in sorted order.
    """

    data_folder = Path(data_folder)

    csv_files = sorted(data_folder.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in: {data_folder}"
        )

    return csv_files


def load_csv_in_chunks(
    file_path,
    chunksize=200_000
):
    """
    Read a large CSV file in chunks.

    This prevents the entire file from being loaded
    into memory at once.
    """

    return pd.read_csv(
        file_path,
        dtype=str,
        chunksize=chunksize,
        on_bad_lines="skip"
    )