from ._django import BASE_DIR, os, config 

SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
POSTGRES = {
    'ENGINE':    'django.db.backends.postgresql_psycopg2',
    'NAME':      config('POSTGRES_DB_NAME'),
    'USER' :     config('POSTGRES_DB_USERNAME'),
    'PASSWORD' : config('POSTGRES_DB_PASSWORD'),
    'HOST' :     config('POSTGRES_DB_HOST') or '127.0.0.1',
    'PORT' :     config('POSTGRES_DB_PORT') or '5432',
}
if config('DB') == 'postgres':
    default = POSTGRES
elif config('DB') == 'mysql':
    default = MYSQL
else:
    default = SQLITE
DATABASES = {
    'default': default,
}



