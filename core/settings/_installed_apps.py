up = [
    'corsheaders',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'dal',
    'dal_select2',
    'admin_auto_filters',
    # 'grappelli',
    # 'jet',
    # 'suit',
    # 'box.wpadmin',
    'box.custom_admin',
    'filebrowser',
    'modeltranslation',
]
django_contrib = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
]
third_party = [
    "mptt",
    "crispy_forms",
    "tinymce",
    'ckeditor',
    'ckeditor_uploader',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'import_export',
    'rosetta',
    # 'django_celery_beat',
    'colorfield',
    # 'adminsortable',
    'adminsortable2',
]
box = [
    'box',
    'box.core',
    'box.seo',
    'box.design',
    'box.contact_form',
    'box.faq',
    'box.imp_exp',
    'box.statistic',
    'box.global_config',
    'box.custom_auth',
    'box.content',
    'box.shop',
    'box.shop.test_shop',
    'box.shop.item',
    'box.shop.order',
    'box.shop.cart',
    'box.shop.liqpay',
    'box.shop.privat24',
    'box.shop.customer',
    'box.shop.novaposhta',
    'box.filemanager',
    'box.blog',
    'box.solo',
    'box.model_search',
    # 'box.constance',

]
installed_apps  = [
    *up,
    *django_contrib,
    *third_party,
    *box,
]

INSTALLED_APPS = installed_apps 



