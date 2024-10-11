from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

# from shops.models import Wishlist
# from shops.serializers import WishlistSerializer
#
#
# # Create your views here.
#
# @extend_schema(tags=["Wishlist"])
# class WishlistModelViewSet(ModelViewSet):
#     queryset = Wishlist.objects.all()
#     serializer_class = WishlistSerializer