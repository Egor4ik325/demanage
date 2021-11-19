from rest_framework import pagination


class MemberPagination(pagination.PageNumberPagination):
    """
    Response data paginzation for member.
    """

    page_size = 20
    max_page_size = 50
    page_query_param = "page"
    page_size_query_param = "page_size"
