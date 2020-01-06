from django.core.mail import send_mail
from datetime import timedelta
from time import sleep 

from celery import shared_task, task
from celery.task import periodic_task
from celery.schedules import crontab

from project.celery import app 



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



# @periodic_task(run_every=crontab(minute='*/1'), name="task_one")
# def task_one():
#     print('TASK ONE IS DONE')


# @periodic_task(run_every=timedelta(seconds=1), name="task_two")
# def task_two():
#     print('TASK TWO IS DONE')


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




# 3 способа создать асинхронную таску - shared_task, task, celery_app.task


# 2 способа создать периодичную таску - periodic_task, CELERY_BEAT_SCHEDULER
