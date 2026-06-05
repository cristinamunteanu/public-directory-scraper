import csv
from pathlib import Path

DEFAULT_CSV_FIELDS = ["name", "url"]


def write_records_csv(records, output_path):
    """Write listing records to a CSV file and return the number of rows written."""
    path = Path(output_path)
    rows = list(records)
    fieldnames = _fieldnames_from_records(rows) or DEFAULT_CSV_FIELDS

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def _fieldnames_from_records(records):
    """Return record keys in first-seen order for CSV headers."""
    fieldnames = []

    for record in records:
        for fieldname in record:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)

    return fieldnames
