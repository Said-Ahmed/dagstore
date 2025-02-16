import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dagstore.settings')
app = Celery('dagstore')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

