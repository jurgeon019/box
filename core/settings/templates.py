import os 
from .default import BASE_DIR
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'box.shop.cart.context_processors.cart_content',
                'box.shop.item.context_processors.categories',
            ],
        },
    },
]

TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'project.context_processors.context',
])