from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.views import APIView


class BoardSearchFilter(SearchFilter):
    search_param = "search"

    def get_search_fields(self, view: APIView, request: Request):
        return ["$title", "@description"]
