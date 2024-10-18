from django.urls import path

from shops.views import BookCreateApiListView, BookUpdateDestroyView

urlpatterns = [
    path('books', BookCreateApiListView.as_view(), name='book-list'),
    path('book/<int:pk>', BookUpdateDestroyView.as_view(), name='book-detail'),
]


