from django.urls import path

from shops.views import  BookUpdateDestroyView, BookListAPIView

urlpatterns = [
    path('book/<int:pk>', BookUpdateDestroyView.as_view(), name='book-detail'),
    path('books', BookListAPIView.as_view(), name='book-list'),
    # path('books/<str:slug>', BookListAPIView.as_view(), name='book-list'),
]


