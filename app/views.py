from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReferenceBook, ReferenceBookElement
from .serializers import ReferenceBookSerializer, ReferenceBookElementSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1


class CustomPagination(PageNumberPagination):
    pagination_class = LargeResultsSetPagination

    @property
    def paginator(self):
        """Экземпляр пагинатора, связанный с view, или «None»"""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """Возвращает одну страницу результатов или «None», если нумерация страниц отключена"""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """Возвращает «Response» в стиле разбивки на страницы, для заданных данных"""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class ReferenceBookAPI(ListAPIView):
    """Получение списка справочников"""
    queryset = ReferenceBook.objects.all()
    serializer_class = ReferenceBookSerializer
    pagination_class = LargeResultsSetPagination


class ActualReferenceBookAPI(APIView, CustomPagination):
    """Получение списка справочников, актуальных на указанную дату"""
    serializer_class = ReferenceBookSerializer

    def get(self, request, created_at):
        ids = []
        reference_book_names = []
        for book in ReferenceBook.objects.filter(created_at__lte=created_at).order_by('-version'):
            if book.name not in reference_book_names:
                reference_book_names.append(book.name)
                ids.append(book.id)

        queryset = ReferenceBook.objects.filter(id__in=ids)
        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class ReferenceBookElementsCurrentVersionAPI(APIView, CustomPagination):
    """Получение элементов заданного справочника текущей версии"""
    serializer_class = ReferenceBookElementSerializer

    def get(self, request, name):
        reference_book = ReferenceBook.objects.filter(name=name).order_by('version').last()
        reference_book_elements = ReferenceBookElement.objects.filter(reference_book=reference_book)

        page = self.paginate_queryset(queryset=reference_book_elements)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class ReferenceBookElementsSpecificVersionAPI(APIView, CustomPagination):
    """Получение элементов заданного справочника указанной версии"""
    serializer_class = ReferenceBookElementSerializer

    def get(self, request, name, version):
        reference_book_elements = ReferenceBookElement.objects.filter(reference_book__name=name,
                                                                      reference_book__version=version)

        page = self.paginate_queryset(queryset=reference_book_elements)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class ValidationReferenceBookElementsCurrentVersionAPI(APIView):
    """Валидация элементов заданного справочника текущей версии"""

    def get(self, request, name, value):
        reference_book = ReferenceBook.objects.filter(name=name).order_by('version').last()
        reference_book_elements = ReferenceBookElement.objects.filter(reference_book=reference_book)

        serializer = ReferenceBookElementSerializer(reference_book_elements, many=True)
        return Response(serializer.data)


class ValidationReferenceBookElementsSpecificVersionAPI(APIView):
    """Валидация элемента заданного справочника по указанной версии"""

    def get(self, request, name, version, value):
        reference_book_elements = ReferenceBookElement.objects.filter(reference_book__name=name, value=value,
                                                                      reference_book__version=version)

        serializer = ReferenceBookElementSerializer(reference_book_elements, many=True)
        return Response(serializer.data)
