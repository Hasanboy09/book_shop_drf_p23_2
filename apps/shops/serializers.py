from django.db.models import Avg
from rest_framework import serializers
from .models import Book, Author, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'stars', 'book']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'image', 'overview', 'features', 'format', 'author', 'reviews']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = AuthorSerializer(instance.author).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['total_reviews'] = instance.reviews.count()
        representation['average_rating'] = instance.reviews.aggregate(Avg('stars'))['stars__avg'] or 0

        return representation
