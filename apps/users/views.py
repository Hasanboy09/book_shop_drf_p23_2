from time import time

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Case, When, BooleanField, F
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import status, mixins
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, CreateAPIView, GenericAPIView, \
    RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from users.email_service import ActivationEmailService
from users.models import User, Address
from users.serializers import AddressListModelSerializer, UserUpdateSerializer, RegisterUserModelSerializer, \
    LoginUserModelSerializer, UserWishlist


@extend_schema(tags=['user'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        return self.request.user


# @extend_schema(tags=['auth'])
# class RegisterCreateAPIView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterUserModelSerializer
#     authentication_classes = ()
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         response = {
#             'message': 'Successfully registered!'
#         }
#         activation_service = ActivationEmailService(user, request._current_scheme_host)
#         activation_service.send_activation_email()
#         return Response(response, status.HTTP_201_CREATED)

@extend_schema(tags=['test'])
class RegisterCreateAPIView(APIView):
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        user = User.objects.first()
        activation_service = ActivationEmailService(user, request._current_scheme_host)
        email = request.GET.get('email')
        if email:
            task = activation_service.send_activation_email(email, priority=request.GET.get('high', None))
            return Response({"task_id": task.id})
        return Response({"msg": "email yuborish kk"})
#     http://localhost:8002/api/v1/users/register?email=sanoqulovhasan113@gmail.com&high=high # high priority
#     http://localhost:8002/api/v1/users/register?email=sanoqulovhasan113@gmail.com # low priority
#     make file dan celery_is_premium ni alohida alohida terminalda ishlatish kerak




@extend_schema(tags=['auth'])
class LoginAPIView(GenericAPIView):
    serializer_class = LoginUserModelSerializer
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['auth'])
class UserActivateAPIView(APIView):
    authentication_classes = ()
    serializer_class = None

    # def get(self, request, uidb64, token):
    #     try:
    #         uid = urlsafe_base64_decode(uidb64).decode()
    #         uid, is_active, _created_at = uid.split('/')
    #         if int(time()) - int(_created_at) > 120:
    #             raise AuthenticationFailed('Havolangiz muddati tugagan')
    #         user = User.objects.get(pk=uid, is_active=is_active)
    #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         user = None
    #
    #     if user and PasswordResetTokenGenerator().check_token(user, token):
    #         user.is_active = True
    #         user.save()
    #         return Response({"message": "User successfully verified!"})
    #     raise AuthenticationFailed('Havola yaroqsiz yoki muddati o‘tgan.')

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            uid, _created_at = uid.split('/')
            if int(time()) - int(_created_at) > 259200:
                raise AuthenticationFailed('Havolangiz muddati tugagan')
            user = User.objects.get(pk=uid, is_active=False)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "User successfully verified!"})
        raise AuthenticationFailed('Havola yaroqsiz yoki muddati o‘tgan.')


@extend_schema(tags=['shops'])
class AddressListCreateAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,  # faqat login qilganlarga ruxsat beradi

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return (
            qs.filter(user=user)
            .annotate(
                shipping_address_id=Case(
                    When(user__shipping_address_id=F('id'), then=False),
                    default=True,
                    output_field=BooleanField()
                ),
                billing_address_id=Case(
                    When(user__billing_address_id=F('id'), then=False),
                    default=True,
                    output_field=BooleanField()
                ),
            )
            .order_by('shipping_address_id', 'billing_address_id', 'first_name', 'last_name')
        )


@extend_schema(tags=['shops'])
class AddressDestroyUpdateAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)  # joriy foydalanuchi address lari
        self._can_delete = qs.count() > 1
        return qs

    def patch(self, request, *args, **kwargs):
        _user: User = request.user
        instance = self.get_object()
        if instance.pk == _user.billing_address_id:
            return Response({"message": "O'zgartirib bo'lmaydi!"})
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance: Address = self.get_object()
        _user: User = request.user
        if self._can_delete and instance.id not in (_user.billing_address_id, _user.shipping_address_id):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "O'chirib bo'lmaydi!"})


@extend_schema(tags=['wishlist'])
class UserWishlistCreateAPIViewDestroyAPIView(CreateAPIView, DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserWishlist
    permission_classes = IsAuthenticated,
