from django.urls import path

from shops.views import BookDetailRetrieveAPIView, BookListAPIView, AuthorDetailRetrieveAPIView

urlpatterns = [
    path('books', BookListAPIView.as_view(), name='book-list'),
    path('book/<str:slug>', BookDetailRetrieveAPIView.as_view(), name='book-detail'),

    # path('authors', AuthorListAPIView.as_view(), name='author-list'),
    path('author/<int:id>', AuthorDetailRetrieveAPIView.as_view(), name='author-detail'),
]
