from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import (
    Category,
    Product,
    Review,
    ConfirmationCode
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductReviewSerializer,
    RegisterSerializer,
    LoginSerializer,
    ConfirmSerializer
)

from django.db.models import Count



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



# PRODUCT REVIEWS


class ProductReviewsView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related(
        'review_set'
    )

    serializer_class = ProductReviewSerializer



# REGISTER


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        code = ConfirmationCode.objects.get(
            user=user
        )

        return Response({
            'message': 'Пользователь создан',
            'confirmation_code': code.code
        })



# LOGIN


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(
            user=user
        )

        return Response({
            'token': token.key
        })



# CONFIRM


class ConfirmUserView(generics.GenericAPIView):
    serializer_class = ConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        user.is_active = True
        user.save()

        Token.objects.get_or_create(
            user=user
        )

        return Response({
            'message': 'Аккаунт подтвержден'
        })