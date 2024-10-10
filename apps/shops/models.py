
from django.db.models import CharField, CASCADE, TextField, ImageField, Model, ForeignKey, JSONField, IntegerField
from mptt.models import MPTTModel, TreeForeignKey

from shared.models import TimeBasedModel


class Section(TimeBasedModel):
    name_image = ImageField(upload_to='shops/categories/name_image/%Y/%m/%d', null=True, blank=True)
    intro = TextField(null=True, blank=True)
    banner = ImageField(upload_to='shops/categories/banner/%Y/%m/%d', null=True, blank=True)


class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='subcategories')
    section = ForeignKey('shops.Section', CASCADE, null=True, blank=True, related_name='categories')

    class MPTTMeta:
        order_insertion_by = ['name']


class Book(TimeBasedModel):
    name = CharField(max_length=250)
    image = ImageField(upload_to='shops/book/image', null=True, blank=True)
    overview = TextField()
    features = JSONField()


class Wishlist(TimeBasedModel):
    book = ForeignKey('shops.Book', CASCADE, null=True, blank=True, related_name='wishlists')
    user = ForeignKey('users.User', CASCADE, null=True, blank=True, related_name='wishlists')


class Card(TimeBasedModel):
    book = ForeignKey('shops.Book', CASCADE, null=True, blank=True, related_name='cards')
    user = ForeignKey('users.User', CASCADE, null=True, blank=True, related_name='cards')
    quantity = IntegerField(default=0)
