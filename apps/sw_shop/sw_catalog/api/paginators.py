from rest_framework.pagination import BasePagination, LimitOffsetPagination, PageNumberPagination, CursorPagination


class StandardPageNumberPagination(PageNumberPagination):
    page_size              = 6
    max_page_size          = 1000
    page_query_param       = 'page_number'
    page_size_query_param  = 'per_page'


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit      = 10
    max_limit          = 1000
    limit_query_param  = 'limit'
    offset_query_param = 'offset'


class StandardCursorPagination(CursorPagination):
    page_size = 10 
    cursor_query_param = 'cursor'
    ordering = '-id'
