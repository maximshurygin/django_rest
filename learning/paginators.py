from rest_framework.pagination import PageNumberPagination


class LearningPaginator(PageNumberPagination):
    page_size = 10
