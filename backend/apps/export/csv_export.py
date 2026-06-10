"""CSV export helper for dashboard table data."""
import csv

from django.http import HttpResponse


def build_csv_response(filename, columns, rows):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)

    keys = [c["key"] for c in columns]
    writer.writerow(keys)
    for row in rows:
        writer.writerow([row.get(key, "") for key in keys])
    return response
