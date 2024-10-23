from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

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


class BookListModelSerializer(ModelSerializer):
    author = AuthorModelSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('title', 'slug', 'author', 'image')


class AuthorDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookDetailModelSerializer(ModelSerializer):
    author = AuthorDetailModelSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            'title', 'slug', 'author', 'image', 'overview', 'used_good_price', 'ebook_price', 'audiobook_price',
            'new_price', 'features')


class BookUpdateDestroyModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'