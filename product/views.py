from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.db.models import Avg, Count

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductReviewSerializer,
    RegisterSerializer,
    LoginSerializer,
    ConfirmSerializer
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


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        code = ConfirmationCode.objects.get(user=user)

        return Response({
            'message': 'Пользователь создан',
            'confirmation_code': code.code
        })
    

class ConfirmUserView(APIView):

    def post(self, request):
        serializer = ConfirmSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        user.is_active = True
        user.save()

        Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Аккаунт подтвержден'
        })
    

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        })