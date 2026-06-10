"""Extract supported dashboard filters from query params."""

FILTER_KEYS = [
    "dateFrom", "dateTo", "region", "status",
    "category", "provider", "organizationType", "sheet",
]


def extract_filters(query_params):
    return {key: query_params.get(key) for key in FILTER_KEYS
            if query_params.get(key)}
