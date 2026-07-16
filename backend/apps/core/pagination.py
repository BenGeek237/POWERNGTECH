"""
POWER NG TECHNOLOGIE — Core Pagination
Standard pagination classes for the API.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Default pagination: 12 items per page.
    Supports ?page_size query param (max 48).
    """
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 48
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {"type": "integer"},
                "total_pages": {"type": "integer"},
                "current_page": {"type": "integer"},
                "next": {"type": "string", "nullable": True},
                "previous": {"type": "string", "nullable": True},
                "results": schema,
            },
        }


class SmallPagination(PageNumberPagination):
    """Pagination for small lists (6 items) — used on homepage sections."""
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 12
