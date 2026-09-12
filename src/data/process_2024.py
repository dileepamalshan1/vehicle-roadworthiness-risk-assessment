from pathlib import Path

import pandas as pd

from .loader import get_csv_files, load_csv_in_chunks
from .cleaner import clean_mot_data

def process_2024(data_folder, output_file):
    """
    Process all 2024 MOT result CSV files.

    Each monthly file is read in chunks, cleaned,
    and then combined into one processed dataset.
    """

    csv_files = get_csv_files(data_folder)

    print(f"Found {len(csv_files)} CSV files.")

    cleaned_chunks = []

    for file_number, file_path in enumerate(csv_files, start=1):

        print(
            f"\nProcessing file {file_number}/{len(csv_files)}: "
            f"{file_path.name}"
        )

        file_rows = 0
        cleaned_rows = 0

        for chunk in load_csv_in_chunks(file_path):

            file_rows += len(chunk)

            cleaned_chunk = clean_mot_data(chunk)

            cleaned_rows += len(cleaned_chunk)

            if not cleaned_chunk.empty:
                cleaned_chunks.append(cleaned_chunk)

        print(f"Raw rows: {file_rows:,}")
        print(f"Cleaned rows: {cleaned_rows:,}")

    if not cleaned_chunks:
        raise ValueError(
            "No valid records were produced."
        )

    print("\nCombining cleaned data...")

    processed_data = pd.concat(
        cleaned_chunks,
        ignore_index=True
    )

    output_file = Path(output_file)
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    processed_data.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nProcessed dataset saved to: "
        f"{output_file}"
    )

    print(
        f"Final rows: "
        f"{len(processed_data):,}"
    )

    return processed_data


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    data_folder = (
        project_root
        / "data"
        / "raw"
        / "2024"
        / "results"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "mot_2024_cleaned.csv"
    )

    process_2024(
        data_folder=data_folder,
        output_file=output_file
    )