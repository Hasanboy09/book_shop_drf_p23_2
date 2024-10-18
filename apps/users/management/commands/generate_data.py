import random
from email.policy import default

from dateutil.tz import UTC
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker import Faker

from shops.models import Author
from users.models import User, Address, Country


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    model_list = {'user', 'author', 'address', 'book'}

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

    def _book(self, count):
        self.stdout.write(self.style.WARNING('Book mal`lumotlari qo`shilmadi'))

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

    def handle(self, *args, **options):
        for name in self.model_list & set(options):
            getattr(self, f"_{name}")(options[name])
        self.stdout.write(self.style.SUCCESS("Barcha ma`lumotlarilumotlar qo`shildi"))
