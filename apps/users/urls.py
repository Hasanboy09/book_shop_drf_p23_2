from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserUpdateView, CustomTokenObtainPairView, UserListAPIView, RegisterCreateAPIView

urlpatterns = [
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),


    path('user-update/<int:pk>' , UserUpdateView.as_view(), name='user_update'),
    path('user-list/', UserListAPIView.as_view(), name='user-list'),


    path('registr/', RegisterCreateAPIView.as_view(), name='register'),
    path('' , )

]

