import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

DEFAULT_CSV_FIELDS = ["name", "url"]
MAX_EXCEL_COLUMN_WIDTH = 60
MIN_EXCEL_COLUMN_WIDTH = 12


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

    _format_excel_sheet(sheet)
    workbook.save(path)
    return len(rows)


def _format_excel_sheet(sheet):
    """Apply simple readable formatting to an Excel worksheet."""
    sheet.freeze_panes = "A2"

    for cell in sheet[1]:
        cell.font = Font(bold=True)

    for column_cells in sheet.columns:
        column_letter = column_cells[0].column_letter
        max_length = max(len(str(cell.value or "")) for cell in column_cells)
        width = min(max(max_length + 2, MIN_EXCEL_COLUMN_WIDTH), MAX_EXCEL_COLUMN_WIDTH)
        sheet.column_dimensions[column_letter].width = width


def _fieldnames_from_records(records):
    """Return record keys in first-seen order for CSV headers."""
    fieldnames = []

    for record in records:
        for fieldname in record:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)

    return fieldnames
