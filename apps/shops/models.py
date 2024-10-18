from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CharField, CASCADE, TextField, ImageField, Model, ForeignKey, JSONField, IntegerField, \
    TextChoices, PositiveSmallIntegerField
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


class Review(TimeBasedModel):
    name = CharField(max_length=255)
    description = TextField()
    stars = PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    book = ForeignKey('shops.Book', CASCADE, related_name='reviews')

    def __str__(self):
        return self.name

    @property
    def star(self):
        return self.stars / 2
