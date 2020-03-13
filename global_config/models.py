from django.db import models 
from django.conf import settings 
from box.solo.models import SingletonModel 
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError



class SiteConfig(SingletonModel):

  # Налаштування сайту 
  DEFAULT_SITE_NAME    = 'Інтернет-магазин'
  DEFAULT_DATE_FORMAT_CHOICES  = (
    ('d.m.Y','d.m.Y'),
  )
  DEFAULT_ADMIN_EMAIL             = 'jurgeon018@gmail.com'
  DEFAULT_TECH_MESSAGE            = 'Алярм! Сайт впав!'
  default_site_og_image_square    = '/static/ogimages/ogimage.png'
  default_site_og_image_rectangle = '/static/ogimages/ogimage.png'
  default_site_favicon            = '/static/favicon.ico'

  SITE_NAME                  = getattr(settings, 'SITE_NAME', DEFAULT_SITE_NAME)
  DATE_FORMAT_CHOICES        = getattr(settings, 'DATE_FORMAT_CHOICES', DEFAULT_DATE_FORMAT_CHOICES)
  ADMIN_EMAIL                = getattr(settings, 'ADMIN_EMAIL', DEFAULT_ADMIN_EMAIL)
  TECH_MESSAGE               = getattr(settings, 'TECH_MESSAGE', DEFAULT_TECH_MESSAGE)
  site_og_image_square       = getattr(settings, 'site_og_image_square', default_site_og_image_square)
  site_og_image_rectangle    = getattr(settings, 'site_og_image_rectangle', default_site_og_image_rectangle)
  site_favicon               = getattr(settings, 'site_favicon', default_site_favicon)

  site_name          = models.CharField(verbose_name=("Ім'я сайту"), max_length=255, default=SITE_NAME)
  date_format        = models.CharField(verbose_name=("Формат дати"), max_length=255, choices=DATE_FORMAT_CHOICES, default=0) 
  admin_email        = models.CharField(verbose_name=("E-mail адміна"), max_length=255,default=ADMIN_EMAIL) 
  site_on            = models.BooleanField(verbose_name=("Вимкнення сайту"), default=True)
  tech_message       = models.TextField(verbose_name=("Технічне повідомлення"), default=TECH_MESSAGE)

  og_image_square    = models.ImageField(verbose_name=("og:image квадрат"),     blank=True, null=True, upload_to='ogimage')
  og_image_rectangle = models.ImageField(verbose_name=("og:image прямокутник"), blank=True, null=True, upload_to='ogimage')
  favicon            = models.ImageField(verbose_name=("Іконка"), blank=True, null=True, upload_to='favicon')

  # captcha
  # ..... captcha 

  def __str__(self):
    return f"{self.id}"
  
  def get_og_image_square_url(self):
    og_image_square_url = self.site_og_image_square
    if self.og_image_square:
      og_image_square_url = self.og_image_square.url
    return og_image_square_url

  def get_og_image_rectangle_url(self):
    og_image_rectangle_url = self.site_og_image_rectangle
    if self.og_image_rectangle:
      og_image_rectangle_url = self.og_image_rectangle.url
    return og_image_rectangle_url

  def get_favicon_url(self):
    favicon_url = self.site_favicon
    if self.favicon:
      favicon_url = self.favicon.url
    return favicon_url

  def get_favicon_type(self):
    ext = self.favicon.split('.')[-1]
    if ext == 'png':
      favicon_type == 'image/png'
    elif ext == 'ico':
      favicon_type == 'x-icon'
    return favicon_type
  @classmethod
  def modeltranslation_fields(cls):
      fields = [
          'og_image_square',
          'og_image_rectangle',
      ]
      return fields
  class Meta:
    verbose_name        = 'Налаштування сайту'
    verbose_name_plural = 'Налаштування сайту'


class NotificationConfig(SingletonModel):
  # admin_mails_language_choices = (
  #   ('',''),
  #   ('',''),
  #   ('',''),
  # )
  admin_mails_language_choices = settings.LANGUAGES
  order_email_notif     = models.CharField(verbose_name=("Email-сповіщення про замовлення"),  max_length=255, null=True, blank=False)
  reverse_email_notif   = models.CharField(verbose_name=("Зворотна адреса сповіщень"),        max_length=255, null=True, blank=False)
  comment_email_notif   = models.CharField(verbose_name=("Email-сповіщення про коментарі"),   max_length=255, null=True, blank=False)
  sender_name           = models.CharField(verbose_name=("Ім'я відправника листа"),           max_length=255, null=True, blank=False)
  admin_mails_language  = models.CharField(verbose_name=("Мова листів адміністратору"),       max_length=255, null=True, blank=False, choices=admin_mails_language_choices)
  auto_comment_approval = models.BooleanField(verbose_name=("Автоматичне схвалення коментарів"), default=True)

  # smpt config
  host = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("Email Host"))

  port = models.SmallIntegerField(
      blank = True, null = True,
      verbose_name = _("Email Port"))

  from_email = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("Default From Email"))

  username = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("Email Authentication Username"))

  password = models.CharField(
      blank = True, null = True,
      max_length = 256, verbose_name = _("Email Authentication Password"))

  use_tls = models.BooleanField(
      default = False, verbose_name = _("Use TLS"))

  use_ssl = models.BooleanField(
      default = False, verbose_name = _("Use SSL"))

  fail_silently = models.BooleanField(
      default = False, verbose_name = _("Fail Silently"))

  timeout = models.SmallIntegerField(
      blank = True, null = True,
      verbose_name = _("Email Send Timeout (seconds)"))

  def clean(self):
      if self.use_ssl and self.use_tls:
          raise ValidationError(
              _("\"Use TLS\" and \"Use SSL\" are mutually exclusive, "
              "so only set one of those settings to True."))


  def __str__(self):
    return f'{self.id}'
  
  class Meta:
    verbose_name        = 'Налаштування сповіщень'
    verbose_name_plural = 'Налаштування сповіщень'


class CalagoueConfig(SingletonModel):
  DEFAULT_ITEMS_PER_PAGE       = 24
  DEFAULT_POSTS_PER_PAGE       = 24
  DEFAULT_MAX_ORDER_ITEMS      = 50
  DEFAULT_MAX_COMPARISON_ITEMS = 50
  DEFAULT_ITEM_MEASURMENT_UNIT  = 'шт'
  DEFAULT_PENNY_DIVIDER = (
    ('dot','.'),
    ('coma',','),
  )
  DEFAULT_THOUSANDS_DIVIDER = (
    ("no",""),
    ("space"," "),
    ("coma",","),
  )
  DEFAULT_ABSENT_ITEMS_POSITION = (
    ("default","default"),
    ("end","end"),
    ("hide","hide"),
  )
  DEFAULT_ABSENT_ITEMS_PREORDER = False 
  DEFAULT_EMPTY_CATEGORIES_VISIBILITY = False 

  DEFAULT_CLEAR_CATALOGUE = False 

  DEFAULT_WATERMARK_HORIZONTAL = 50
  DEFAULT_WATERMARK_VERTICAL = 50


  ITEMS_PER_PAGE               = getattr(settings, 'ITEMS_PER_PAGE', DEFAULT_ITEMS_PER_PAGE) 
  POSTS_PER_PAGE               = getattr(settings, 'POSTS_PER_PAGE', DEFAULT_POSTS_PER_PAGE) 
  MAX_ORDER_ITEMS              = getattr(settings, 'MAX_ORDER_ITEMS', DEFAULT_MAX_ORDER_ITEMS)
  MAX_COMPARISON_ITEMS         = getattr(settings, 'MAX_COMPARISON_ITEMS', DEFAULT_MAX_COMPARISON_ITEMS)
  ITEM_MEASURMENT_UNIT         = getattr(settings, 'ITEM_MEASURMENT_UNIT', DEFAULT_ITEM_MEASURMENT_UNIT)
  PENNY_DIVIDER                = getattr(settings, 'PENNY_DIVIDER', DEFAULT_PENNY_DIVIDER)
  THOUSANDS_DIVIDER            = getattr(settings, 'THOUSANDS_DIVIDER', DEFAULT_THOUSANDS_DIVIDER)
  ABSENT_ITEMS_POSITION        = getattr(settings, 'ABSENT_ITEMS_POSITION', DEFAULT_ABSENT_ITEMS_POSITION)
  ABSENT_ITEMS_PREORDER        = getattr(settings, 'ABSENT_ITEMS_PREORDER', DEFAULT_ABSENT_ITEMS_PREORDER)
  EMPTY_CATEGORIES_VISIBILITY  = getattr(settings, 'EMPTY_CATEGORIES_VISIBILITY', DEFAULT_EMPTY_CATEGORIES_VISIBILITY)

  CLEAR_CATALOGUE              = getattr(settings, 'CLEAR_CATALOGUE', DEFAULT_CLEAR_CATALOGUE)

  WATERMARK_HORIZONTAL         = getattr(settings, 'WATERMARK_HORIZONTAL', DEFAULT_WATERMARK_HORIZONTAL)
  WATERMARK_VERTICAL           = getattr(settings, 'WATERMARK_VERTICAL', DEFAULT_WATERMARK_VERTICAL)


  items_per_page               = models.PositiveIntegerField(verbose_name=("Товарів на сторінці сайту"), null=True, default=ITEMS_PER_PAGE)
  max_order_items              = models.PositiveIntegerField(verbose_name=("Максимум товарів у замовленні"), default=POSTS_PER_PAGE)
  posts_per_page               = models.PositiveIntegerField(verbose_name=("Статей на сторінці блоґу"), default=MAX_ORDER_ITEMS)
  max_comparison_items         = models.PositiveIntegerField(verbose_name=("Максимум товарів у порівнянні"), default=MAX_COMPARISON_ITEMS)
  item_measurment_unit         = models.CharField(verbose_name=("Одиниці вимірювання товарів"), default=ITEM_MEASURMENT_UNIT, max_length=255)
  penny_divider                = models.CharField(verbose_name=("Роздільник копійок"), choices=PENNY_DIVIDER, default=0, max_length=255)
  thousands_divider            = models.CharField(verbose_name=("Роздільник тисяч"), choices=THOUSANDS_DIVIDER, default=0, max_length=255)
  absent_items_position        = models.CharField(verbose_name=("Відсутні товари "), choices=ABSENT_ITEMS_POSITION, default=0, max_length=255)
  absent_items_preorder        = models.BooleanField(verbose_name=("Передзамовлення відсутніх товарів"), default=ABSENT_ITEMS_PREORDER)
  empty_categories_visibility  = models.BooleanField(verbose_name=("Відображати порожні категорії"), default=EMPTY_CATEGORIES_VISIBILITY)

  clear_catalogue              = models.BooleanField(verbose_name=(" Очистити каталог товарів "), default=CLEAR_CATALOGUE)
  # https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  watermark_horizontal         = models.PositiveIntegerField(verbose_name=("Горизонтальне положення водяного знака (лівіше-правіше)"), blank=True, null=True)#, max_value=100, min_value=1)
  watermark_vertical           = models.PositiveIntegerField(verbose_name=("Вертикальне положення водяного знака (вижче-нижче)"), blank=True, null=True)#, max_value=100, min_value=1)

  def __str__(self):
    return f'{self.id}'
  
  class Meta:
    verbose_name        = 'Налаштування каталогу'
    verbose_name_plural = 'Налаштування каталогу'

