from celery import shared_task, task
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import datetime, date, time, timedelta
from .utils import * 


@shared_task
def load_warehouses_from_json():
    print('load_warehouses_from_json')
    handle_np(action='refresh', content='warehouses', type='from_api')
    handle_np(action='refresh', content='warehouses', type='from_json')

# @shared_task
# def load_warehouses_to_json():
#     print('load_warehouses_to_json')
    # handle_np(action='refresh', content='warehouses', type='from_api')





# @periodic_task(run_every=timedelta(seconds=100))
@periodic_task(run_every=timedelta(days=30)) 
def load_warehouses():
    print('load_warehouses')
    load_warehouses_from_json.delay()





@periodic_task(run_every=timedelta(seconds=10))
def test_faina():
    print('celery works!')
    return 'celery works!'












