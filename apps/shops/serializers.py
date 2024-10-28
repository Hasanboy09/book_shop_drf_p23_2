from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from shared.utils import get_dollar_currency
from shops.models import Author, Book
from users.serializers import AuthorModelSerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'bio']


#
# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['id', 'name', 'description', 'stars', 'book']

#
# class BookSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer()
#     reviews = ReviewSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'image', 'overview', 'features', 'format', 'author', 'reviews']

# def to_representation(self, instance):
#     representation = super().to_representation(instance)
#     representation['author'] = AuthorSerializer(instance.author).data
#     representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
#     representation['total_reviews'] = instance.reviews.count()
#     representation['average_rating'] = instance.reviews.aggregate(Avg('stars'))['stars__avg'] or 0
#
#     return representation


class AuthorDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        exclude = ()


class AuthorListModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        exclude = ()


class BookUpdateDestroyModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookListModelSerializer(ModelSerializer):
    author = AuthorModelSerializer(many=True, read_only=True)
    price_in_currency = SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'slug', 'author', 'image', 'price_in_currency')

    def get_price_in_currency(self, obj):
        # Xuddi `BookDetailModelSerializer` dagi kabi valyutani qaytaradi # noqa
        return BookDetailModelSerializer.get_price_in_currency(self, obj)


class BookDetailModelSerializer(ModelSerializer):
    author = AuthorDetailModelSerializer(many=True, read_only=True)
    price_in_currency = SerializerMethodField()

    class Meta:
        model = Book
        exclude = ()

    def get_price_in_currency(self, obj):
        usd_rate, success = get_dollar_currency()  # utils.py
        if not success or not usd_rate:
            return obj.used_good_price
        user = self.context['request'].user
        if user.is_authenticated and hasattr(user, 'currency') and user.currency:
            if user.currency == "USD":
                return obj.used_good_price
            else:
                return obj.used_good_price * usd_rate
        return obj.used_good_price
