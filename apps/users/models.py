from django.contrib.auth.models import AbstractUser
from django.db.models import ManyToManyField


class User(AbstractUser):
    wishlist = ManyToManyField('shops.Book', blank=True)
