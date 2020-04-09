import os 
from ._django import BASE_DIR
from ._installed_apps import INSTALLED_APPS 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'box.core.context_processors.context',
            ],
            'loaders':[
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                "admin_tools.template_loaders.Loader",
            ]
        },
    },
]


if 'box.apps.sw_shop.cart' in INSTALLED_APPS:
    TEMPLATES[0]['OPTIONS']['context_processors'].extend([
        'box.apps.sw_shop.cart.context_processors.cart_content',
    ])

if 'box.apps.sw_shop.item' in INSTALLED_APPS:
    TEMPLATES[0]['OPTIONS']['context_processors'].extend([
        # 'box.sw_shot.item.context_processors.context',
    ])

if 'box.apps.sw_payment' in INSTALLED_APPS:
    TEMPLATES[0]['OPTIONS']['context_processors'].extend([
        # '',
    ])

