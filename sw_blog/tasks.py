from celery import task


@task()
def task_number_one():
    print('one')

@task()
def task_number_two():
    print('two')




