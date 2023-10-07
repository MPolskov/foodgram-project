from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    '''
    Пагинатор.

    Количество выводимых записей определяется параметром запроса "limit"
    (по умолчанию = 10).
    '''

    page_size = 10
    page_size_query_param = 'limit'
