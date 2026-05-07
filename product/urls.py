from django.urls import path
from .views import *


urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),

    # Products
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),

    # Reviews
    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),

    # Products with reviews
    path('products/reviews/', ProductReviewsView.as_view()),
]