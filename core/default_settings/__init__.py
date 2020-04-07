from ._admin_toolbar import * 
from ._auth import * 
from ._crispy_forms import * 
from ._ckeditor import * 
from ._corsheaders import * 
from ._django import * 
from ._drf import * 
from ._email import * 
from ._installed_apps import * 
from ._import_export import * 
from ._middleware import * 
from ._rest import * 
from ._templates import * 
from ._tinymce import * 
from ._translation import * 
from ._wp import * 





























"""
#in core.settings

from box.core.default_settings import * 
INSTALLED_APPS  = [
    *priority_third_party,
    *django_contrib,
    *third_party,
    *box_core,
    *box_shop,
    *box_payment,
    *box_blog,
    'project',
]
TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'project.context_processors.context',
])
MIDDLEWARE.extend([
    'project.middlewares.Middleware',
])
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'margo_db',
    'USER' : 'jurgeon018',
    'PASSWORD' : '69018',
    'HOST' : '127.0.0.1',
    'PORT' : '5432',
}
STATIC_SITEMAP_PAGES = [
    'index',
    'contact',
    'blog',
    'about',
]
PROJECT_CORE_MULTILINGUAL_URLS = [
    'project.urls',
]
PROJECT_CORE_URLS = [
    'project.api.urls',
]
ROOT_URLCONF     = 'project.core.urls'
WSGI_APPLICATION = 'project.core.wsgi.application'










in core.celery 

from celery import Celery 
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app = Celery('core', backend='amqp', broker='amqp://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




in core.tasks 

from django.core.mail import send_mail
from datetime import timedelta
from time import sleep 

from celery import shared_task, task
from celery.task import periodic_task
from celery.schedules import crontab

from core.celery import app 



@shared_task
def sleepy(duration):
    sleep(duration)
    return None 


@shared_task
def send_email_task():
    print('1')
    send_mail(
        subject='worked!',
        message='worked!!!',
        from_email='jurgeon018@gmail.com',
        recipient_list=['jurgeon018@gmail.com',],
        fail_silently=False,
    )
    print('2')
    return None



@periodic_task(run_every=crontab(minute='*/1'), name="task_one")
def task_one():
    print('TASK ONE IS DONE')


@periodic_task(run_every=timedelta(seconds=1), name="task_two")
def task_two():
    print('TASK TWO IS DONE')


@shared_task
def task_three():
    print('TASK THREE IS DONE')


@shared_task
def task_four():
    print('TASK FOUR IS DONE')


@task() 
def task_five():
    print('TASK FIVE IS DONE')


@app.task
def task_six():
    print('TASK SIX IS DONE')







@task()
def task_number_one():
    print('one')

@task()
def task_number_two():
    print('two')






3 способа создать асинхронную таску - shared_task, task, celery_app.task


2 способа создать периодичную таску - periodic_task, CELERY_BEAT_SCHEDULER

"""
