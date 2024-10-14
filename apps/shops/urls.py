from unittest.mock import patch

from django.urls import path

from shops.views import CountryListView, AddressListView

# from shops.views import WishlistModelViewSet
#
urlpatterns = [
    # path('wishlist/<int:pk>' , WishlistModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='wishlist'),
    path('country-list' , CountryListView.as_view() , name='country-list'),
    path('address' , AddressListView.as_view() , name='address-list'),
]