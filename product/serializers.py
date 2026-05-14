from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.db.models import Avg

from .models import Category, Product, Review, ConfirmationCode


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                'Название категории слишком короткое'
            )

        if value.isdigit():
            raise serializers.ValidationError(
                'Название не может состоять только из цифр'
            )

        return value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = 'all'

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                'Название товара слишком короткое'
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Цена должна быть больше 0'
            )
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                'Описание слишком короткое'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_text(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'Отзыв слишком короткий'
            )
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Рейтинг должен быть от 1 до 5'
            )
        return value


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(source='review_set', many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'reviews', 'rating']

    def get_rating(self, obj):
        avg = obj.review_set.aggregate(avg=Avg('stars'))['avg']
        return round(avg, 2) if avg else 0
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False
    )

        ConfirmationCode.objects.create(user=user)

        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )

        if not user:
            raise serializers.ValidationError(
                'Неверный логин или пароль'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Аккаунт не подтвержден'
            )

        attrs['user'] = user
        return attrs
    

class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(
                username=attrs['username']
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь не найден'
            )

        try:
            confirm = ConfirmationCode.objects.get(
                user=user
            )
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError(
                'Код подтверждения не найден'
            )

        if confirm.code != attrs['code']:
            raise serializers.ValidationError(
                'Неверный код'
            )

        attrs['user'] = user
        return attrs