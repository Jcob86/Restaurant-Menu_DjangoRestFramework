import os 
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurant.settings')

celery = Celery('Restaurant')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()

celery.conf.beat_schedule = {
    'add': {
        'task': 'menu.tasks.add',
        'schedule': crontab(minute='*/1'),
        'args': (20, 20)
    },
}