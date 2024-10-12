from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'


class RegisterSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = 'email', 'password', 'confirm_password', 'first_name'
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        confirm_password = data.get('confirm_password')
        password = data.get('password')
        if confirm_password != password:
            raise ValidationError('Passwords do not match!')
        return data

    # def validate(self, attrs):
    #     confirm_password = attrs.pop('confirm_password')
    #     if confirm_password != attrs.get('password'):
    #         raise ValidationError('Passwords did not match!')
    #     attrs['password'] = make_password(confirm_password)
    #     return attrs

