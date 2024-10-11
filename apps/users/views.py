from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView

from users.models import User
from users.serializers import UserSerializer


@extend_schema(tags=["users"])
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=["register"])
class RegisterCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


