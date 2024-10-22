from django.contrib.auth.models import AbstractUser
from django.db.models import ManyToManyField, EmailField, BooleanField, ForeignKey, CASCADE, IntegerField, CharField, \
    Model, OneToOneField, RESTRICT

from shared.models import TimeBasedModel
from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    is_active = BooleanField(default=False)
    shipping_address = OneToOneField('users.Address', RESTRICT, null=True, blank=True, related_name='shipping_user')
    billing_address = OneToOneField('users.Address', RESTRICT, null=True, blank=True, related_name='billing_user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    wishlist = ManyToManyField('shops.Book', blank=True, related_name='wishlist')


class Cart(TimeBasedModel):
    book = ForeignKey('shops.Book', CASCADE, null=True, blank=True, related_name='cards')
    user = ForeignKey('users.User', CASCADE, null=True, blank=True, related_name='cards')
    quantity = IntegerField(default=0)
    format = CharField(max_length=250)
    condition = CharField(max_length=250)
    seller = CharField(max_length=250)
    ship_from = CharField(max_length=250)


class Address(Model):
    first_name = CharField(max_length=250)
    last_name = CharField(max_length=250)
    country = ForeignKey('users.Country', CASCADE)
    city = CharField(max_length=50)
    address = CharField(max_length=250)
    state = CharField(max_length=50)
    postal_code = CharField(max_length=50)
    phone_number = CharField(max_length=50)
    user = ForeignKey('users.User', CASCADE, related_name='addresses')


class Country(Model):
    name = CharField(max_length=255)
    code = CharField(max_length=255)


    def __str__(self):
        return self.name
