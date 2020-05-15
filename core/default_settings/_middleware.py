MIDDLEWARE = [
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    
    'box.core.middleware.PutParsingMiddleware',
    'box.core.middleware.JSONParsingMiddleware',
    'box.core.middleware.DisableCSRF',
]



