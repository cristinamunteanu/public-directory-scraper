import csv
from pathlib import Path

from openpyxl import Workbook

DEFAULT_CSV_FIELDS = ["name", "url"]


def write_records(records, output_path):
    """Write records to a supported output file and return the number of rows."""
    suffix = Path(output_path).suffix.lower()

    if suffix == ".csv":
        return write_records_csv(records, output_path)

    if suffix == ".xlsx":
        return write_records_excel(records, output_path)

    raise ValueError("output file must end with .csv or .xlsx")


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


def write_records_excel(records, output_path):
    """Write listing records to an Excel file and return the number of rows written."""
    path = Path(output_path)
    rows = list(records)
    fieldnames = _fieldnames_from_records(rows) or DEFAULT_CSV_FIELDS
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "records"
    sheet.append(fieldnames)

    for row in rows:
        sheet.append([row.get(fieldname, "") for fieldname in fieldnames])

    workbook.save(path)
    return len(rows)


def _fieldnames_from_records(records):
    """Return record keys in first-seen order for CSV headers."""
    fieldnames = []

    for record in records:
        for fieldname in record:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)

    return fieldnames
