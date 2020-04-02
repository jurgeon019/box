up = [
    'corsheaders',
    'box.sw_admin',  
    # 'admin_tools', 'admin_tools.theming', 'admin_tools.menu', 'admin_tools.dashboard',

    'dal',
    'dal_select2',
    'admin_auto_filters',
    # 'filebrowser',
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
    'colorfield',
    'adminsortable2',
    "rest_framework",
    "rangefilter",
]
box = [

    'box',
    'box.blog',
    'box.contact_form',
    'box.content',
    'box.core',
    'box.sw_auth',
    'box.design',
    'box.faq',
    #  'box.filemanager',
    'box.global_config',
    'box.imp_exp',
    'box.model_search',
    'box.novaposhta',

    'box.payment',
    'box.payment.liqpay',
    'box.payment.privat24',
    'box.payment.wayforpay',
    'box.payment.interkassa',

    'box.seo',

    'box.sw_shop',
    'box.sw_shop.test_shop',
    'box.sw_shop.item',
    'box.sw_shop.order',
    'box.sw_shop.cart',
    'box.sw_shop.customer',

    
    'box.solo',
    'box.statistic',

]
installed_apps  = [
    *up,
    *django_contrib,
    *third_party,
    *box,
]

INSTALLED_APPS = installed_apps 



