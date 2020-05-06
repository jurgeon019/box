from celery import shared_task, task
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import datetime, date, time, timedelta
from .views import * 



# @shared_task
# def add(x, y):
#     for i in range(100):
#         print(i)
#     return x+y


# @shared_task
# def func2(x, y):
#     print('hello')
#     print('world')
#     return x+y*2



# @periodic_task(run_every=timedelta(seconds=10))
@periodic_task(run_every=timedelta(hours=24)) 
def parse_currencies_from_pb():
    print('parse_currencies_from_pb')
    parse_currencies()








