from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

from shared.paginations import CustomPageNumberPagination
from shops.models import Book
from shops.serializers import BookListModelSerializer, BookDetailModelSerializer, BookUpdateDestroyModelSerializer


#
# @extend_schema(tags=['book'])
# class BookCreateApiListView(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer




@extend_schema(tags=['book'])
class BookListAPIView(ListCreateAPIView):
    queryset = Book.objects.order_by('-id')
    serializer_class = BookListModelSerializer
    pagination_class = CustomPageNumberPagination



@extend_schema(tags=['book'])
class BookDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailModelSerializer
    lookup_field = 'slug'  # instead of using pk



@extend_schema(tags=['book'])
class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUpdateDestroyModelSerializer


