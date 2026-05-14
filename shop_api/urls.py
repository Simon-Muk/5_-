from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/confirm/', ConfirmUserView.as_view()),
    
]
