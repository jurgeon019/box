from django.core.mail import send_mail
from django.conf import settings


CURRENT_DOMEN = settings.CURRENT_DOMEN


def send_order_mail():
  send_mail(
    subject = 'Order form Received',
    # message = get_template('contact_message.txt').render({'message':message}),
    message = f'Було отримано замовлення товарів. Перейдіть по цій ссилці: {CURRENT_DOMEN}/admin/core/order/',
    from_email = settings.DEFAULT_FROM_EMAIL,
    recipient_list = [settings.DEFAULT_FROM_EMAIL],#, email],
    fail_silently=True,
  )
