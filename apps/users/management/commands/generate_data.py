import random

from tkinter.font import names

from dateutil.tz import UTC
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from shops.models import Author, Section, Category, Book, Review
from users.models import User, Address, Country, Cart


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    model_list = {'user', 'author', 'address', 'section' ,'review' , 'cart'}

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.f = Faker()
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        for model in self.model_list:
            parser.add_argument(f"--{model}", type=int, default=0)

    def _user(self, count):
        user_list = list()
        for _ in range(count):
            user_list.append(User(
                email=self.f.email(),
                name=self.f.name(),
                is_active=self.f.boolean(),
                password=make_password(self.f.password()),
                date_joined=self.f.date_time(tzinfo=UTC)
            ))
        User.objects.bulk_create(user_list)
        self.stdout.write(self.style.SUCCESS(f"User ma`lumotlari {count} tadan qo`shildi"))


    def _author(self, count):
        author_list = list()
        for _ in range(count):
            author_list.append(Author(
                name=self.f.name(),
                bio=self.f.text(),
            ))
        Author.objects.bulk_create(author_list)
        self.stdout.write(self.style.SUCCESS(f"Author ma`lumotlari {count} tadan qo`shildi"))

    def _address(self, count):
        address_list = list()
        for _ in range(count):
            address_list.append(Address(
                first_name=self.f.first_name(),
                last_name=self.f.last_name(),
                country_id=Country.objects.order_by("?").values_list('id', flat=True).first(),
                city=self.f.city(),
                address=self.f.address(),
                state=self.f.state(),
                postal_code=self.f.postalcode(),
                phone_number=self.f.phone_number(),
                user_id=User.objects.order_by('?').values_list('id', flat=True).first()
            ))
        Address.objects.bulk_create(address_list)
        self.stdout.write(self.style.SUCCESS(f"Address ma`lumotlari {count} tadan qo`shildi"))

    def _section(self, count):
        section_list = list()
        for _ in range(count):
            section_list.append(Section(
                name_image=self.f.image_url(),
                intro=self.f.text(),
                banner = self.f.image_url()
            ))
        Section.objects.bulk_create(section_list)
        self.stdout.write(self.style.SUCCESS(f"Section ma`lumotlari {count} tadan qo`shildi"))


    def _review(self, count):
        review_list = list()
        for _ in range(count):
            review_list.append(Review(
                name=self.f.name(),
                description=self.f.text(),
                stars = self.f.numerify(),
                book_id=Book.objects.order_by("?").values_list('id', flat=True).first(),
            ))
        Review.objects.bulk_create(review_list)
        self.stdout.write(self.style.SUCCESS(f"Review ma`lumotlari {count} tadan qo`shildi"))


    # def _category(self, count):
    #     category_list = []
    #
    #     parent_section = Section.objects.order_by("?").first()
    #     parent_ = Category.objects.create(name=self.f.word(), section=parent_section)
    #     categories = [parent_]
    #     for _ in range(count):
    #         parent_category = random.choice(categories)
    #         section = Section.objects.order_by("?").first()
    #         category_list.append(Category(
    #             name=self.f.word(),
    #             parent=parent_category,
    #             section=section,
    #         ))
    #     Category.objects.bulk_create(category_list)
    #     self.stdout.write(self.style.SUCCESS(f"Category ma`lumotlari {count} tadan qo`shildi"))

    # def _book(self, count):
    #     book_list = list()
    #     book_format = random.choice([Book.Format.HARDCOVER, Book.Format.PAPERBACK])
    #
    #     for _ in range(count):
    #         book_list.append(Book(
    #             name=self.f.name(),
    #             image_url=self.f.file_extension(),
    #             overview=self.f.text(),
    #             features=self.f.json(),
    #             format=book_format,
    #             author_id=Author.objects.order_by('?').values_list('id', flat=True).first(),
    #         ))
    #     Book.objects.bulk_create(book_list)
    #     self.stdout.write(self.style.SUCCESS(f"Book ma`lumotlar {count} qo`shildi"))
    #

    def _cart(self,count):
        cart_list = list()
        for _ in range(count):
            cart_list.append(Cart(
                book_id=Book.objects.order_by("?").values_list('id', flat=True).first(),
                user_id=User.objects.order_by("?").values_list('id', flat=True).first(),
                quantity=self.f.numerify(),
                format=self.f.text(),
                condition=self.f.text(),
                seller=self.f.name(),
                ship_from=self.f.text(),
            ))
        Cart.objects.bulk_create(cart_list)
        self.stdout.write(self.style.SUCCESS(f"Cart ma`lumotlari {count} tadan qo`shildi"))




    def handle(self, *args, **options):
        for name in self.model_list & set(options):
            getattr(self, f"_{name}")(options[name])
        self.stdout.write(self.style.SUCCESS("Barcha ma`lumotlarilumotlar qo`shildi"))
