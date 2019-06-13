"""
Paginations classes.

This file contains classes for the chat_room application.
"""

from rest_framework.pagination import PageNumberPagination


class MessagesPagination(PageNumberPagination):
    """
    Pagination for messages.

    This class provide change page size via request.
    """

    page_size_query_param = 'page_size'
    max_page_size = 10
