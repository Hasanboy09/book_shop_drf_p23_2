from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from shops.models import Book
from shops.serializers import BookSerializer

@extend_schema(tags=['book'])
class BookCreateApiListView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@extend_schema(tags=['book'])
class BookUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
