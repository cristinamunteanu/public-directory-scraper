import csv
from pathlib import Path

CSV_FIELDS = ["name", "url"]


def write_records_csv(records, output_path):
    path = Path(output_path)
    rows = list(records)

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)
