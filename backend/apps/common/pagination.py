"""Pagination that emits the spec's {success, data, pagination, message} envelope."""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    page_size = 20
    max_page_size = 200

    def get_page_number(self, request, paginator):
        # Spec uses 0-based page indexes; DRF is 1-based internally.
        raw = request.query_params.get(self.page_query_param, 0)
        try:
            return int(raw) + 1
        except (TypeError, ValueError):
            return 1

    def get_paginated_response(self, data):
        return Response({
            "success": True,
            "data": data,
            "pagination": {
                "page": self.page.number - 1,
                "size": self.get_page_size(self.request),
                "totalElements": self.page.paginator.count,
                "totalPages": self.page.paginator.num_pages,
            },
            "message": None,
        })
