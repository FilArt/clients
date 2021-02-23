from collections import OrderedDict

from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UsersPagination(PageNumberPagination):
    page_size_query_param = "itemsPerPage"
    max_page_size = 100

    def get_paginated_response(self, data):
        suma = sum(self.page.paginator.object_list.annotate(x=Count('bids')).values_list('x', flat=True))
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('suma', suma),
        ]))


class AttachmentsPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 10
