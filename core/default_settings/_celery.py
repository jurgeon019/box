# CELERY_BROKER_URL = 'amqp://127.0.0.1//'



# REDIS_HOST = 'localhost'
# REDIS_PORT = '6379'
# BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
# CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

# CELERY_TIMEZONE = 'Asia/Makassar'
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379//'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_BEAT_SCHEDULE = {
    # 'third-task':{
    #     'task':'app1.tasks.task_three',
    #     'schedule': 2.0,
    #     # 'args': 
    # },
    # 'fourth-task':{
    #     'task':'app1.tasks.task_four',
    #     'schedule': 3.0,
    #     # 'args': 
    # },
    # 'fifth-task':{
    #     'task':'app1.tasks.task_five',
    #     'schedule': crontab(minute=59, hour=23),
    #     # 'schedule': crontab(minute=0, hour='*/3,10-19'),
    #     # 'schedule': crontab(hour=16, day_of_week=5),
    #     # 'schedule': 3600.0,
    #     # 'schedule': solar('sunset', -37.81753, 144.96715),
    # },
    # 'sixth-task':{
    #     'task':'core.tasks.create_races_every_night',
    #     'schedule':3.0
    # }

# }





"""
commands:

celery -A core worker -l info
celery -A core beat -l info 

or 

celery -A core worker --beat 

or 

celery -A core worker -l info --beat



in core.celery 

from celery import Celery 
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app = Celery('core', backend='amqp', broker='amqp://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




in appname.tasks 

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
