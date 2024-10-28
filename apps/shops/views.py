from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView

from shared.paginations import CustomPageNumberPagination
from shops.models import Book, Author
from shops.serializers import BookListModelSerializer, BookDetailModelSerializer, BookUpdateDestroyModelSerializer, \
    AuthorDetailModelSerializer, AuthorListModelSerializer


#
# @extend_schema(tags=['book'])
# class BookCreateApiListView(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


@extend_schema(tags=['shops'])
class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListModelSerializer
    pagination_class = CustomPageNumberPagination


@extend_schema(tags=['shops'])
class BookDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailModelSerializer
    lookup_field = 'slug'


@extend_schema(tags=['book'])
class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUpdateDestroyModelSerializer


@extend_schema(tags=['author'])
class AuthorDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailModelSerializer
    lookup_field = 'id'

