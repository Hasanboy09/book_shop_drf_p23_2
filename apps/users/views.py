from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserModelSerializer, RegisterSerializer


@extend_schema(tags=['user-list'])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


@extend_schema(tags=["users"])
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=["register"])
class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class =RegisterSerializer
    permission_classes = (permissions.AllowAny,)



class CustomTokenObtainPairView(TokenObtainPairView):
    pass
