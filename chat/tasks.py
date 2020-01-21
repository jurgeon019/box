from django.core.mail import send_mail
from datetime import timedelta
from time import sleep 

from celery import shared_task, task
from celery.task import periodic_task
from celery.schedules import crontab

from core.celery import app 


