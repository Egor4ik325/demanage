from rest_framework import pagination


class BoardPagination(pagination.PageNumberPagination):
    """
    Response data pagination for board.
    """

    page_size = 10
    max_page_size = 30
    page_query_param = "page"
    page_size_query_param = "page_size"
