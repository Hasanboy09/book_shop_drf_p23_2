from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserModelSerializer, RegisterSerializer, LoginSerializer


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
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=["login"])
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]

    # def post(self, request):
    #     serializer = LoginSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
    #         if user:
    #             token, created = Token.objects.get_or_create(user=user)
    #             return Response({'token': [token.key], "Sucsses": "Login SucssesFully"},
    #                             status=status.HTTP_201_CREATED)
    #         return Response({'Massage': 'Invalid Username and Password'}, status=401)
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    pass
