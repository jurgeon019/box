from django.utils.translation import gettext_lazy as _
from django.db import models 
from django.conf import settings 
from django.core.exceptions import ValidationError

from box.core import settings as core_settings 
from box.core.sw_solo.models import SingletonModel
from . import settings as sw_global_config_settings 

from tinymce import HTMLField
from colorfield.fields import ColorField
from box.core.models import AbstractRecipientEmail


class GlobalRecipientEmail(AbstractRecipientEmail):
  config = models.ForeignKey(
    verbose_name=_("Глобальні налаштування"), to="sw_global_config.GlobalConfig", 
    on_delete=models.CASCADE, related_name='emails'
  )
  class Meta:
      verbose_name = _('емейл для всіх сповіщень')
      verbose_name_plural = _("емейли для всіх сповіщень")


class SeoScript(models.Model):
  POSITION_CHOICES = (
    ("head_top","Після відкриваючого head"),
    ("body_top","Після відкриваючого body"),
    ("head_bottom","Перед закриваючим head"),
    ("body_bottom","Перед закриваючим body"),
  )
  setting  = models.ForeignKey(
    to="sw_global_config.GlobalConfig", 
    on_delete=models.CASCADE, related_name='scripts',
  )
  code     = models.TextField(verbose_name=_("Код для вставлення"))
  name     = models.CharField(verbose_name=_("Назва коду"), max_length=255)
  position = models.CharField(
    verbose_name=_("Положення коду на сторінці"), max_length=255, 
    choices=POSITION_CHOICES
  )

  def __str__(self):
    return f'{self.name}, {self.position}, {self.code}'

  class Meta:
    verbose_name = ('Код')
    verbose_name_plural = ('Коди')


class GlobalTag(models.Model):
  color    = ColorField(
    verbose_name=_("Колір"), 
  )
  name     = models.CharField(
    verbose_name=_("Назва"), max_length=255, blank=False, null=False
  )
  config   = models.ForeignKey(
    verbose_name=_("Глобальні налаштування"), on_delete=models.CASCADE,
    to='sw_global_config.GlobalConfig', null=True, blank=False, 
  )

  def __str__(self):
    return f"{self.name}"
  
  @classmethod 
  def modeltranslation_fields(cls): return ['name',] 

  class Meta: 
    verbose_name = ('тег')
    verbose_name_plural = ('теги')


class GlobalLabel(models.Model):
  text  = models.CharField(
    verbose_name=_('Текст'), max_length=255,
  )
  code  = models.SlugField(
    verbose_name=_("Код"), unique=True, null=True, blank=True,
  )

  @classmethod
  def modeltranslation_fields(cls): return ['text']

  def __str__(self): 
    return f"{self.text}"
  
  def save(self, *args, **kwargs):
    if self.text:
      self.text = self.text.strip().lower()
    super().save(*args, **kwargs)

  class Meta:
    verbose_name = _('мітка')
    verbose_name_plural = _('мітки')


class GlobalMarker(models.Model):
  name  = models.CharField(
    verbose_name=_('Назва'), max_length=255
  )
  code  = models.SlugField(
    verbose_name=_("Код"), unique=True, null=True, blank=True
  )

  def __str__(self): 
    return f"{self.name}"
  def save(self, *args, **kwargs):
    if self.name:
      self.name = self.name.strip().lower()
    super().save(*args, **kwargs)

  @classmethod
  def modeltranslation_fields(cls): return ['name']

  class Meta:
    verbose_name = _('маркер')
    verbose_name_plural = _('маркери')


class GlobalConfig(SingletonModel):
  
  def get_recipient_list(self):
    return list(GlobalRecipientEmail.objects.filter(
      is_active=True, config=self,
    ).values_list('email', flat=True))
  
  ROBOTS_VARS = (
    ("index, nofollow",  "index, nofollow"),
    ("index, follow",    "index, follow"),
    ("noindex, nofollow","noindex, nofollow"),
    ("noindex, follow",  "noindex, follow"),
  )
  robots = models.CharField(
    verbose_name=_("Meta Robots"), max_length=255, blank=True, null=True,
    choices=ROBOTS_VARS, default=sw_global_config_settings.META_ROBOTS
  )
  robots_txt = models.TextField(verbose_name=_('robots.txt'), blank=True, null=True)
  favicon  = models.ImageField(
    verbose_name=_("Фавікон сайту"), blank=True, null=True, upload_to='favicon', 
    help_text=_("Допустимі розширення зображень png, gif, jpg, jpeg, ico"), 
    default=sw_global_config_settings.FAVICON
  )
  og_image_square    = models.ImageField(
    verbose_name=_("og:image квадрат"),     
    blank=True, null=True, upload_to='ogimage',
    default=sw_global_config_settings.OGIMAGE_SQUARE,
  )
  og_image_rectangle = models.ImageField(
    verbose_name=_("og:image прямокутник"), 
    blank=True, null=True, upload_to='ogimage',
    default=sw_global_config_settings.OGIMAGE_RECTANGLE,
  )

  @property
  def favicon_type(self):
    name = self.favicon.url
    ext = name.split('.')[-1].strip()
    if ext == 'png':
      favicon_type = 'image/png'
    elif ext == 'ico':
      favicon_type = 'x-icon'
    return favicon_type
  
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
      help_text=_(" "), 
      default=settings.EMAIL_USE_TLS,
  )
  use_ssl = models.BooleanField(
      verbose_name = _("EMAIL_USE_SSL"),
      help_text=_(" "), 
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
  
  @classmethod
  def modeltranslation_fields(cls):        
      return [
          'og_image_square',
          'og_image_rectangle',
      ]

  def __str__(self):
      return f"{self.id}"

  class Meta:
      verbose_name = _('Глобальні налаштування')
      verbose_name_plural = verbose_name
