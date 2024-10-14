import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('proj')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
