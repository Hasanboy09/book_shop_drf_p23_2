from rest_framework.serializers import ModelSerializer

from shops.models import Country, Address


# from shops.models import Wishlist

# class WishlistSerializer(ModelSerializer):
#     class Meta:
#         model = Wishlist
#         fields = '__all__'




class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country'] = instance.country
        return representation