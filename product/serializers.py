from django.db.models import Count
from django.db.models import Avg
from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class ProductReviewSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(source='review_set', many=True)
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'reviews', 'rating']

    def get_rating(self, obj):
        avg = obj.review_set.aggregate(avg=Avg('stars'))['avg']
        return round(avg, 2) if avg else 0


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'starts']