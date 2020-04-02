from django.db import models 
from django.utils.translation import gettext_lazy as _
from box.core import settings as core_settings 
from box.solo.models import SingletonModel
from box.content.models import Text

from tinymce import HTMLField
from colorfield.fields import ColorField


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


#TODO: перенести в global_config 

