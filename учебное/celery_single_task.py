from celery import Celery 
from time import time 


# https://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#conf-database-result-backend
# sqlite (filename)
result_backend = 'db+sqlite:///results.sqlite'
# mysql
result_backend = 'db+mysql://scott:tiger@localhost/foo'
# postgresql
result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'
# oracle
result_backend = 'db+oracle://scott:tiger@127.0.0.1:1521/sidname'
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#conf-redis-result-backend

     
app = Celery(
    'tasks', 
    broker='amqp://127.0.0.1//',
    backend="db+sqlite:///db.sqlite3",
) 

@app.task
def reverse(string):
    time(10)
    print('sdfsdsf')
    return string[::-1]




# Asynchronous Tasks in Python - Getting Started With Celery
# https://www.youtube.com/watch?v=fg-JfZBetpM


# Asynchronous Tasks in Python - Celery Backend Tutorial
# https://www.youtube.com/watch?v=UHveawwmi-o


# terminal 1 
# sudo apt-get install rabbitmq-server 
# sudo service rabbitmq-server restart
# sudo rabbitmqctl status 

# terminal 2 
# celery -A tasks worker --loglevel=info

# terminal 3
# python 
# from tasks import *
# reverse.delay('blablabla')
# result = reverse.delay('blablabla')
# result.status
# >>> 'PENDING'
# result.ready()
# >>> False
# # 10 seconds later
# >>> 'SUCCESS'
# result.ready()
# >>> True

# terminal 2
# >>> albalbalb

# dbsqlitebrowser 
# >>> db.sqlite3
