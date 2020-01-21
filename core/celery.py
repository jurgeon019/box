from celery import Celery 
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app = Celery('core', backend='amqp', broker='amqp://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()