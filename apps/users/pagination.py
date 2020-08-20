from rest_framework.pagination import PageNumberPagination


class UsersPagination(PageNumberPagination):
    page_size_query_param = 'itemsPerPage'
    max_page_size = 100
