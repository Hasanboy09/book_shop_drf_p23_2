from django.urls import path

from shops.views import BookDetailRetrieveAPIView, BookListAPIView, BookRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('book/<str:slug>', BookDetailRetrieveAPIView.as_view(), name='book-detail'),
    path('books', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-list'),
]


