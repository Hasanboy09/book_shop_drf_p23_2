from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from shops.models import Country, Address
from shops.serializers import CountrySerializer, AddressSerializer


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


@extend_schema(tags=["country-list"])
class CountryListView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer



@extend_schema(tags=["address"])
class AddressListView(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

