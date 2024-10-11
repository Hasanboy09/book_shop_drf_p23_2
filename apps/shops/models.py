from django.db.models import CharField, CASCADE, TextField, ImageField, Model, ForeignKey, JSONField, IntegerField, \
    TextChoices
from mptt.models import MPTTModel, TreeForeignKey

from shared.models import TimeBasedModel


class Country(Model):
    name = CharField(max_length=255)
    code = CharField(max_length=255)  # belgi # noqa

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
    class Format(TextChoices):
        HARDCOVER = 'Hardcover', 'hardcover'
        PAPERBACK = 'Paperback', 'paperback'

    name = CharField(max_length=250)
    image = ImageField(upload_to='shops/book/image', null=True, blank=True)
    overview = TextField()
    features = JSONField()
    format = CharField(max_length=10, choices=Format.choices, default=Format.HARDCOVER)
    author = ForeignKey('shops.Author', CASCADE)

class Author(Model):
    name = CharField(max_length=250)
    bio = TextField()


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
    country = ForeignKey('shops.Country', CASCADE)
    city = CharField(max_length=50)
    address = CharField(max_length=250)
    state = CharField(max_length=50)
    email_code = CharField(max_length=50)
    phone_number = CharField(max_length=50)
    user = ForeignKey('users.User', CASCADE, related_name='addresses')
