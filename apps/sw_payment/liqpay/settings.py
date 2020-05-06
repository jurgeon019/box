from django.conf import settings 


LIQPAY_PUBLIC_KEY  = getattr(settings, 'LIQPAY_PUBLIC_KEY', None)
LIQPAY_PRIVATE_KEY = getattr(settings, 'LIQPAY_PRIVATE_KEY', None)

LIQPAY_SANDBOX_PUBLIC_KEY  = getattr(settings, 'LIQPAY_SANDBOX_PUBLIC_KEY', None)
LIQPAY_SANDBOX_PRIVATE_KEY = getattr(settings, 'LIQPAY_SANDBOX_PRIVATE_KEY', None)



