app:
	python manage.py startapp users
mig:
	python manage.py makemigrations
	python manage.py migrate

user:
	python manage.py createsuperuser

celery:
	celery -A root worker -l INFO

loaddata:
	python manage.py loaddata country


data:
	python3 manage.py generate_data --user 5 --author 5  --address 5  --book 5  --section 5  --cart 5  --review 5 --category 5

