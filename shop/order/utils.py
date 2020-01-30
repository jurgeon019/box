from django.core.mail import send_mail
from django.conf import settings


CURRENT_DOMEN = settings.CURRENT_DOMEN


def send_order_mail():
  send_mail(
    subject = 'Було отримано замовлення',
    # message = get_template('contact_message.txt').render({'message':message}),
    message = f'Було отримано замовлення товарів. Перейдіть по цій ссилці: {CURRENT_DOMEN}/admin/order/order/',
    from_email = settings.EMAIL_HOST_USER,
    recipient_list = [settings.EMAIL_HOST_USER],
    fail_silently=False,
  )



