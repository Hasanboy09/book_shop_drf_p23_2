from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from shared.paginations import CustomPageNumberPagination
from shops.models import Book
from shops.serializers import BookSerializer, BookListModelSerializer


#
# @extend_schema(tags=['book'])
# class BookCreateApiListView(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


@extend_schema(tags=['book'])
class BookUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@extend_schema(tags=['book'])
class BookListAPIView(ListCreateAPIView):
    queryset = Book.objects.order_by('-id')
    serializer_class = BookListModelSerializer
    pagination_class = CustomPageNumberPagination
