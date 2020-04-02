from django.utils.translation import gettext_lazy as _
from django.db import models 
from django.conf import settings 
from box.solo.models import SingletonModel 
from django.core.exceptions import ValidationError

from box.core import settings as core_settings 
from box.solo.models import SingletonModel
from box.content.models import Text

from tinymce import HTMLField
from colorfield.fields import ColorField





__all__ = [
  'SiteConfig',
  'NotificationConfig',
  'CatalogueConfig',
  'DesignConfig',
]

from box.payment.liqpay import settings as liqpay_settings

class SiteConfig(SingletonModel):
  liqpay_public_key   = models.TextField(_("Публічний ключ лікпею"), blank=False, null=False, default=liqpay_settings.LIQPAY_PUBLIC_KEY)
  liqpay_private_key  = models.TextField(_("Приватний ключ лікпею"), blank=False, null=False, default=liqpay_settings.LIQPAY_PRIVATE_KEY)
  # captcha_type_choices = (
  #   ("default","default"),
  #   ("v2","v2"),
  #   ("v3","v3"),
  #   ("invisible","invisible"),
  # )
  # captcha_type        = models.CharField(_("Тип капчі"), blank=False, null=False, max_length=100, choices=captcha_type_choices, default=0)
  # captcha_v2_public   = models.TextField(_("Ключ"), blank=False, null=False, default=settings.CAPTCHA_V2_PUBLIC)
  # captcha_v2_secret   = models.TextField(_("Приватний ключ"), blank=False, null=False, default=settings.CAPTCHA_V2_SECRET)
  # captcha_v3_public   = models.TextField(_("Ключ"), blank=False, null=False, default=settings.CAPTCHA_V3_PUBLIC)
  # captcha_v3_secret   = models.TextField(_("Приватний ключ"), blank=False, null=False, default=settings.CAPTCHA_V3_SECRET)
  # captcha_v3_humanity = models.PositiveIntegerField(_("Людяність"), blank=False, null=False, default=0.5)
  
  @classmethod
  def modeltranslation_fields(cls):
      fields = [
      ]
      return fields
  class Meta:
    verbose_name        = _('Налаштування сайту')
    verbose_name_plural = _('Налаштування сайту')


class NotificationConfig(SingletonModel):

  default_emails = getattr(settings, 'DEFAULT_RECIPIENTS', ['jurgeon018@gmail.com',])
  default_emails = ','.join(default_emails)

  admin_mails_language_choices = settings.LANGUAGES

  order_subject = models.TextField(
    verbose_name=("Текст сповіщення про замовлення"), 
    blank=False, null=False, 
    default='Отримано замовлення товарів',
  )
  contact_subject = models.TextField(
    verbose_name=("Текст сповіщення про контакти"), 
    blank=False, null=False, 
    default='Отримано контактну форму',
  )
  review_subject = models.TextField(
    verbose_name=("Текст сповіщення про відгуки"), 
    blank=False, null=False, 
    default='Отримано відгук до товару',
  )
  comment_subject = models.TextField(
    verbose_name=("Текст сповіщення про коментарі"), 
    blank=False, null=False, 
    default='Отримано коментар до блогу',
  )


  order_emails  = models.TextField(
    verbose_name=("замовлення"),
    help_text=("Email-адреси для сповіщень про замовлення товарів. Перечислити через кому."),  
    max_length=255, null=False, blank=False, 
    default=default_emails
  )
  contact_emails  = models.TextField(
    verbose_name=("контакти"),
    help_text=("Email-адреси для сповіщень про форми звязку. Перечислити через кому."),  
    null=False, blank=False, 
    default=default_emails
  )
  review_emails  = models.TextField(
    verbose_name=("відгуки"),
    help_text=("Email-адреси для сповіщень про відгуки про товар. Перечислити через кому."),  
    null=False, blank=False, 
    default=default_emails
  )
  comment_emails  = models.TextField(
    verbose_name=("коментарі"),
    help_text=("Email-адреси для сповіщень про коментарі в блозі. Перечислити через кому."),   
    null=False, blank=False, 
    default=default_emails
  )
  other_emails  = models.TextField(
    verbose_name=("інше"),
    help_text=("Email-адреси для загальних сповіщень. Перечислити через кому."),   
    null=False, blank=False, 
    default=default_emails
  )

  reverse_emails_help_text = ('Email-адреси на яку будуть дублюватися всі листи. Перечислити через кому.')
  reverse_emails = models.TextField(
    verbose_name=("Зворотні Email-адреси"),   
    help_text=reverse_emails_help_text,
    null=True, blank=True, 
  )

  sender_name = models.CharField(
    verbose_name=("Ім'я відправника листа"),           
    max_length=255, null=True, blank=True
  )

  admin_mails_language  = models.CharField(
    verbose_name=("Мова листів адміністратору"),       
    max_length=255, null=True, blank=True, 
    choices=admin_mails_language_choices
  )


  def get_data(self, field, *args, **kwargs):
    lst = ['order','contact','review','comment','other', 'reverse',]
    if field not in lst:
      raise Exception('поле мусить бути в %s' % lst)
    
    emails  = getattr(self, f'{field}_emails').replace(' ', '').split(',')
    subject = getattr(self, f'{field}_subject', None)
    return  {'subject':subject, 'emails':emails}


  auto_comment_approval = models.BooleanField(verbose_name=_("Автоматичне схвалення коментарів до блогу"), default=True)
  auto_review_approval  = models.BooleanField(verbose_name=_("Автоматичне схвалення відгуків до товару"),  default=True)

  # smpt config
  host = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("EMAIL_HOST"),
      help_text=_("Сервер"), 
      default=settings.EMAIL_HOST,
  )

  port = models.SmallIntegerField(
      blank = True, null = True,
      verbose_name = _("EMAIL_PORT"),
      help_text=_("Порт"), 
      default=settings.EMAIL_PORT,
  )

  from_email = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("DEFAULT_FROM_EMAIL"),
      help_text=_("Почта відправки листів"), 
      default=settings.DEFAULT_FROM_EMAIL,
  )

  username = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("EMAIL_HOST_USER"),
      help_text=_("Логін"), 
      default=settings.EMAIL_HOST_USER,
  )

  password = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("EMAIL_HOST_PASSWORD"),
      help_text=_("Пароль"), 
      default=settings.EMAIL_HOST_PASSWORD,
  )

  use_tls = models.BooleanField(
      verbose_name = _("EMAIL_USE_TLS"),
      help_text=_(""), 
      default=settings.EMAIL_USE_TLS,
  )

  use_ssl = models.BooleanField(
      verbose_name = _("EMAIL_USE_SSL"),
      help_text=_(""), 
      default=settings.EMAIL_USE_SSL,
  )

  fail_silently = models.BooleanField(
      default = False, verbose_name = _("fail_silently"),
      help_text=_("Помилка при невдалій відправці")
  )

  timeout = models.SmallIntegerField(
      blank = True, null = True,
      verbose_name = _("timeout"),
      help_text=_("Таймаут в секундах")
  )

  def clean(self):
      if self.use_ssl and self.use_tls:
          raise ValidationError(
              _("\"Use TLS\" and \"Use SSL\" are mutually exclusive, "
              "so only set one of those settings to True."))

  def __str__(self):
    return f'{self.id}'
  
  class Meta:
    verbose_name        = 'Налаштування сповіщень'
    verbose_name_plural = verbose_name


class CatalogueConfig(SingletonModel):
  PENNY_DIVIDER = (
    ('dot','.'),
    ('coma',','),
  )
  THOUSANDS_DIVIDER = (
    ("no","без роздільника: 1234567 грн"),
    ("space","пробіл: 1 234 456 грн "),
    ("coma","кома: 1,234,456"),
  )
  ABSENT_ITEMS_POSITION = (
    ("default","default"),
    ("end","end"),
    ("hide","hide"),
  )

  items_per_page               = models.PositiveIntegerField(verbose_name=_("Товарів на сторінці сайту"), null=True, default=24)
  posts_per_page               = models.PositiveIntegerField(verbose_name=_("Статей на сторінці блоґу"), default=50)
  # max_order_items              = models.PositiveIntegerField(verbose_name=_("Максимум товарів у замовленні"), default=24)
  # max_comparison_items         = models.PositiveIntegerField(verbose_name=_("Максимум товарів у порівнянні"), default=50)
  # item_measurment_unit         = models.CharField(verbose_name=_("Одиниці вимірювання товарів"), default="шт", max_length=255)
  # penny_divider                = models.CharField(verbose_name=_("Роздільник копійок"), choices=PENNY_DIVIDER, default=0, max_length=255)
  # thousands_divider            = models.CharField(verbose_name=_("Роздільник тисяч"), choices=THOUSANDS_DIVIDER, default=0, max_length=255)
  # absent_items_position        = models.CharField(verbose_name=_("Відсутні товари "), choices=ABSENT_ITEMS_POSITION, default=0, max_length=255)
  # absent_items_preorder        = models.BooleanField(verbose_name=_("Передзамовлення відсутніх товарів"), default=False)
  # empty_categories_visibility  = models.BooleanField(verbose_name=_("Відображати порожні категорії"), default=False)

  clear_catalogue              = models.BooleanField(verbose_name=_(" Очистити каталог товарів "), default=False)
  # https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  # watermark_horizontal         = models.PositiveIntegerField(verbose_name=_("Горизонтальне положення водяного знака (лівіше-правіше)"), blank=True, null=True)#, max_value=100, min_value=1)
  # watermark_vertical           = models.PositiveIntegerField(verbose_name=_("Вертикальне положення водяного знака (вижче-нижче)"), blank=True, null=True)#, max_value=100, min_value=1)

  def __str__(self):
    return f'{self.id}'
  
  def __save__(self, *args, **kwargs):
    if self.clear_catalogue:
      Item.objects.all().delete()
    super().save(*args, **kwargs)
  
  class Meta:
    verbose_name        = _('Налаштування каталогу')
    verbose_name_plural = _('Налаштування каталогу')



class DesignConfig(SingletonModel):

    logo     = models.ImageField(verbose_name=_("Логотип сайту"), blank=True, null=True, help_text=("Допустимі розширення зображень png, gif, jpg, jpeg, ico"), default='')
    favicon  = models.ImageField(verbose_name=_("Фавікон сайту"), blank=True, null=True, upload_to='favicon', help_text=("Допустимі розширення зображень png, gif, jpg, jpeg, ico"), default='') 
    og_image_square    = models.ImageField(verbose_name=_("og:image квадрат"),     blank=True, null=True, upload_to='ogimage')
    og_image_rectangle = models.ImageField(verbose_name=_("og:image прямокутник"), blank=True, null=True, upload_to='ogimage')


    @property
    def favicon_type(self):
      name = core_settings.FAVICON
      if self.favicon:
        name = self.favicon.url
      ext = name.split('.')[-1].strip()
      if ext == 'png':
        favicon_type = 'image/png'
      elif ext == 'ico':
        favicon_type = 'x-icon'
      return favicon_type
  
    @property
    def favicon_url(self):
      favicon_url = core_settings.FAVICON
      if self.favicon:
        favicon_url = self.favicon.url
      return favicon_url

    @property
    def og_image_square_url(self):
      og_image_square_url = core_settings.OGIMAGE_SQUARE
      if self.og_image_square:
        og_image_square_url = self.og_image_square.url
      return og_image_square_url

    @property
    def og_image_rectangle_url(self):
      og_image_rectangle_url = core_settings.OGIMAGE_RECTANGLE
      if self.og_image_rectangle:
        og_image_rectangle_url = self.og_image_rectangle.url
      return og_image_rectangle_url

    # colour_buttons                = ColorField(verbose_name=_("Колір кнопок"), blank=True, null=True)
    # colour_buttons_text           = ColorField(verbose_name=_("Колір тексту на кнопках"), blank=True, null=True)
    # colour_buttons_hover          = ColorField(verbose_name=_("Колір кнопок по наведенню"), blank=True, null=True)
    # colour_buttons_text_hover     = ColorField(verbose_name=_("Колір тексту на кнопках по наведенню"), blank=True, null=True)
    # colour_main                   = ColorField(verbose_name=_("Основний корпоративний колір"), blank=True, null=True)
    # colour_additional             = ColorField(verbose_name=_("Додатковий корпоративний колір"), blank=True, null=True)
    # colour_main_background        = ColorField(verbose_name=_("Колір тексту на основному корпоративному фоні"), blank=True, null=True)
    # colour_additional_background  = ColorField(verbose_name=_("Колір тексту на додатковому корпоративному фоні"), blank=True, null=True)
    # colour_background             = ColorField(verbose_name=_("Колір фону сайту"), blank=True, null=True)

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'logo',
            'og_image_square',
            'og_image_rectangle',
        ]
        return fields
  
    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = _('Налаштування дизайну')
        verbose_name_plural = verbose_name

