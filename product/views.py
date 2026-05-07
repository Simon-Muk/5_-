from rest_framework import generics
from django.db.models import Avg, Count

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductReviewSerializer
)


# CATEGORY

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.annotate(
        products_count=Count('product')
    )
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# PRODUCT

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# REVIEW

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# PRODUCTS WITH REVIEWS

class ProductReviewsView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('review_set')
    serializer_class = ProductReviewSerializer