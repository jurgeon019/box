from django.db import models 
from django.utils.translation import gettext_lazy as _
from django.conf import settings 

from box.solo.models import SingletonModel
from box.page.models import PageFeature

from tinymce import HTMLField
from colorfield.fields import ColorField


class DesignConfig(SingletonModel):

    logo     = models.ImageField(verbose_name=("Логотип сайту"), blank=True, null=True, help_text=("Допустимі розширення зображень png, gif, jpg, jpeg, ico"), default='')
    favicon  = models.ImageField(verbose_name=("Фавікон сайту"), blank=True, null=True, upload_to='favicon', help_text=("Допустимі розширення зображень png, gif, jpg, jpeg, ico"), default='') 
    og_image_square    = models.ImageField(verbose_name=("og:image квадрат"),     blank=True, null=True, upload_to='ogimage')
    og_image_rectangle = models.ImageField(verbose_name=("og:image прямокутник"), blank=True, null=True, upload_to='ogimage')
    map      = models.TextField(verbose_name=("Мапа в контактах"), blank=True, null=True, help_text=("Необхідно вставити код з Google maps або Яндекс карти"))

    # time     = HTMLField(verbose_name=("Чаc роботи"), null=True, blank=True, )
    # delivery = HTMLField(verbose_name=("Способи доставки(в картці товару)"), blank=True, null=True, )
    # payment  = HTMLField(verbose_name=("Способи оплати(в картці товару)"), blank=True, null=True, )

    @property
    def favicon_type(self):
      name = settings.FAVICON
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
      favicon_url = settings.FAVICON
      if self.favicon:
        favicon_url = self.favicon.url
      return favicon_url

    @property
    def og_image_square_url(self):
      og_image_square_url = settings.OGIMAGE_SQUARE
      if self.og_image_square:
        og_image_square_url = self.og_image_square.url
      return og_image_square_url

    @property
    def og_image_rectangle_url(self):
      og_image_rectangle_url = settings.OGIMAGE_RECTANGLE
      if self.og_image_rectangle:
        og_image_rectangle_url = self.og_image_rectangle.url
      return og_image_rectangle_url

    # colour_buttons                = ColorField(verbose_name=("Колір кнопок"), blank=True, null=True)
    # colour_buttons_text           = ColorField(verbose_name=("Колір тексту на кнопках"), blank=True, null=True)
    # colour_buttons_hover          = ColorField(verbose_name=("Колір кнопок по наведенню"), blank=True, null=True)
    # colour_buttons_text_hover     = ColorField(verbose_name=("Колір тексту на кнопках по наведенню"), blank=True, null=True)
    # colour_main                   = ColorField(verbose_name=("Основний корпоративний колір"), blank=True, null=True)
    # colour_additional             = ColorField(verbose_name=("Додатковий корпоративний колір"), blank=True, null=True)
    # colour_main_background        = ColorField(verbose_name=("Колір тексту на основному корпоративному фоні"), blank=True, null=True)
    # colour_additional_background  = ColorField(verbose_name=("Колір тексту на додатковому корпоративному фоні"), blank=True, null=True)
    # colour_background             = ColorField(verbose_name=("Колір фону сайту"), blank=True, null=True)

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
        verbose_name = ('Налаштування дизайну')
        verbose_name_plural = verbose_name


class DesignAddress(models.Model):
  design  = models.ForeignKey("design.DesignConfig", verbose_name=_("Конфіг"), on_delete=models.CASCADE)
  address = models.CharField(_('Адреса'), max_length=255)


class DesignPhone(models.Model):
  design = models.ForeignKey("design.DesignConfig", verbose_name=_("Конфіг"), on_delete=models.CASCADE)
  phone = models.CharField(_('Телефон'), max_length=255)


class DesignEmail(models.Model):
  design = models.ForeignKey("design.DesignConfig", verbose_name=_("Конфіг"), on_delete=models.CASCADE)
  email = models.CharField(_('Емайл'), max_length=255)


class DesignSocial(models.Model):
  design = models.ForeignKey("design.DesignConfig", verbose_name=_("Конфіг"), on_delete=models.CASCADE)
  link   = models.CharField(verbose_name=("Ссилка"), max_length=255)

