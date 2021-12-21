from rest_framework.filters import OrderingFilter


class BoardOrderingFilter(OrderingFilter):
    ordering_param = "ordering"
    ordering_fields = ["created"]
