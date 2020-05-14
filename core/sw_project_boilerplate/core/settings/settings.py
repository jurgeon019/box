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
AUTH_USER_MODEL = 'project.ProjectUser'
TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'project.context_processors.context',
])
MIDDLEWARE.extend([
    # 'project.middlewares.Middleware',
])
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': 'margo_db',
#     'USER' : 'jurgeon018',
#     'PASSWORD' : '69018',
#     'HOST' : '127.0.0.1',
#     'PORT' : '5432',
# }
STATIC_SITEMAP_PAGES = [
    # 'index',
    # 'contact',
    # 'blog',
    # 'about',
]
PROJECT_CORE_MULTILINGUAL_URLS = [
    'project.multilingual_urls',
]
PROJECT_CORE_URLS = [
    'project.urls',
]
ROOT_URLCONF     = 'box.core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

