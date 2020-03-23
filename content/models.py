from django.db import models 
from tinymce import HTMLField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 
from django.core.exceptions import ValidationError

from box.core.helpers import get_admin_url
from box.core.models import AbstractPage
from .abstract_models import AbstractContent, AbstractText, AbstractLink
from .utils import validate_phone_number


class Page(AbstractPage):
  class Meta:
    verbose_name        = _("cторінка")
    verbose_name_plural = _("cторінки")

  def __str__(self):
    return f'{self.code}, {self.meta_title}'



class Map(AbstractContent):
  html = models.TextField(
    verbose_name=_("iframe"), 
    blank=False, null=False,
  )
  class Meta:
    verbose_name = _("карта")
    verbose_name_plural = _("карти")
    ordering = [
      '-updated',
    ]


class Img(AbstractContent):
  image   = models.ImageField(verbose_name=_("Картинка"), upload_to="page/", null=True, blank=True, help_text=("Картинка, яка буде відображатися на сайті"))
  alt     = models.CharField(verbose_name=_("Альт"), blank=True, null=True, max_length=255)

  class Meta:
    verbose_name        = _("картинка")
    verbose_name_plural = _("картинки")
    ordering = [
      '-updated',
    ]

  @classmethod
  def modeltranslation_fields(cls):
    fields = [
      'alt',
    ]
    return fields

  @property
  def image_url(self):
    image_url = '' 
    if self.image:
      image_url = self.image.url 
    return image_url


class Text(AbstractText):
  class Meta:
    verbose_name=_("переклад")
    verbose_name_plural=_("переклади")
    ordering = [
      '-updated',
    ]


class Address(AbstractText):
  class Meta:
    verbose_name=_("переклад")
    verbose_name_plural=_("переклади")
    ordering = [
      '-updated',
    ]


class Tel(AbstractLink):
  class Meta:
    verbose_name = _("телефонний номер")
    verbose_name_plural = _("телефонні номера")
    ordering = [
      '-updated',
    ]
  def clean(self):
    valid = validate_phone_number(self.href)
    if not valid:
      raise ValidationError(_("Номер має бути без пробілів, без літер, без спецсимволів, починатися з + та містити в собі 13 символів. Приклад: +380957891234."))
    

class Mailto(AbstractLink):
  class Meta:
    verbose_name = _("емейл")
    verbose_name_plural = _("емейли")
    ordering = [
      '-updated',
    ]


class Link(AbstractLink):
  text = models.CharField(
    verbose_name=_("Текст посилання"), max_length=255,
    blank=False, null=False,
  )
  href     = models.CharField(
    verbose_name=_("Фактичне посилання"), max_length=255,
    blank=False, null=False,
  )
  
  class Meta:
    verbose_name = _("посилання")
    verbose_name_plural = _("посилання")
    ordering = [
      '-updated',
    ]


# class Social(models.Model):
#   img 
#   href 












from django.db import models 
from django.conf import settings 
from django.utils.translation import gettext_lazy as _

from box.core.models import BaseMixin

class Slide(
    BaseMixin,
    ):
    page      = models.ForeignKey(verbose_name=_("Сторінка"), to="page.Page", related_name="slides", on_delete=models.SET_NULL, blank=True, null=True)
    image     = models.ImageField(verbose_name=_("Зображення"), blank=False, null=False)
    slider    = models.ForeignKey(verbose_name=_("Слайдер"), to='slider.Slider', related_name='slides', on_delete=models.SET_NULL, null=True, blank=False) 
    name      = models.CharField(verbose_name=_("Назва"), max_length=255, blank=True, null=True)  
    alt       = models.CharField(verbose_name=_("Назва зображення(alt)"), max_length=255, blank=True, null=True) 
    title     = models.CharField(verbose_name=_("Вспливаюча підказка(title)"), max_length=255, blank=True, null=True)  
    text      = models.TextField(verbose_name=_("Текст"), blank=True, null=True)  

    # TODO: настройки для лобецького
    # DISPLAY_CHOICES = (
    #     ("no_text", "Зображення без тексту"),
    #     ("text_toned", "Текст на зображенні з тонуванням"),
    #     ("text_right", "Текст праворуч, зображення зліва"),
    #     ("text_left", "Текст зліва, зображення праворуч"),
    # )
    # display   = models.CharField(verbose_name=_("Варіант відображення"), choices=DISPLAY_CHOICES, max_length=255, default=0)  
    # mw_desc   = models.IntegerField(verbose_name=_("Максимальна ширина дексктопі"), default=1050)  
    # mh_desc   = models.IntegerField(verbose_name=_("Максимальна висота на дексктопі"), default=400)  
    # mw_mob    = models.IntegerField(verbose_name=_("Максимальна ширина мобілках"), default=500)  
    # mh_mob    = models.IntegerField(verbose_name=_("Максимальна висота на мобілках"), default=320)  

    def __str__(self):
        return f'{self.id}'
    
    
    def save(self, *args, **kwargs):
        if not self.page:
            if self.slider:
                if self.slider.page:
                    self.page = self.slider.page 
        super().save(*args, **kwargs)
    
    @property
    def slider_name(self):
        slider_name = ''
        if self.slider:
            slider_name = self.slider.name 
        return slider_name 
    
    @property
    def image_url(self):
        image_url = settings.NO_SLIDER_IMAGE_URL
        if self.image:
            image_url = self.image.url
        return image_url 
    
    def get_image_url(self):
        image_url = settings.NO_SLIDER_IMAGE_URL
        if self.image:
            image_url = self.image.url
        return image_url 
    
    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'alt',
            'title',
            'text',
        ]
        return fields

    class Meta:
        verbose_name = ('Слайд')
        verbose_name_plural = ('Слайди')
        ordering = ['order']
    



class Slider(BaseMixin):
    name = models.CharField(verbose_name=_("Назва"), max_length=255, blank=True, null=True)
    page = models.ForeignKey(
        verbose_name=("Сторінка"), 
        to="page.Page", 
        related_name='sliders', 
        blank=True,
        null=True, 
        on_delete=models.SET_NULL,
    )

    # category = models.ForeignKey(
    #     verbose_name=("Категорія"), 
    #     to="item.ItemCategory", 
    #     related_name='sliders', 
    #     blank=True,
    #     null=True, 
    #     on_delete=models.SET_NULL,
    # )

    # brand = models.ForeignKey(
    #     verbose_name=("Бренд"), 
    #     to="item.ItemBrand", 
    #     related_name='sliders', 
    #     blank=True,
    #     null=True, 
    #     on_delete=models.SET_NULL,
    # )

    # item = models.ForeignKey(
    #     verbose_name=("Товар"), 
    #     to="item.Item", 
    #     related_name='sliders', 
    #     blank=True,
    #     null=True, 
    #     on_delete=models.SET_NULL,
    # )
    
    # TODO: відображення на сторінках
    # pages          = models.ManyToManyField(verbose_name=_("Сторінки"), to="page.Page", related_name='sliders', blank=True)
    # categories     = models.ManyToManyField(verbose_name=_("Категорії"), to="item.ItemCategory", related_name='sliders', blank=True)
    # brands         = models.ManyToManyField(verbose_name=_("Бренди"), to="item.ItemBrand", related_name='sliders', blank=True)
    # items          = models.ManyToManyField(verbose_name=_("Товари"), to="item.Item", related_name='sliders', blank=True)
    
    # all_pages      = models.BooleanField(verbose_name=_("Відображати групу на всіх сторінках"), default=False)
    # all_categories = models.BooleanField(verbose_name=_("Відображати групу на всіх категоріях"), default=False)
    # all_brands     = models.BooleanField(verbose_name=_("Відображати групу на всіх брендах"), default=False)
    # all_items      = models.BooleanField(verbose_name=_("Відображати групу на всіх товарах"), default=False)
    # TODO: розібратись шо таке шорткод
    # code          = models.SlugField(verbose_name=_("id групи банера"), max_length=255, blank=True, null=True)
    # shortcode     = models.SlugField(verbose_name=_("Назва шорткода"), max_length=255, blank=True, null=True)
    # is_individual = models.BooleanField(verbose_name=_("Індивідуальний шорткод"), blank=True, null=True)
    # # TODO: настройки для лобецького
    # SPEED_HELP = ("Застосовується при включеному автоперелистуванні слайдів. Вказується в мілісекундах.")
    # as_slider  = models.BooleanField(verbose_name=_('Група банерів як слайдер'), default=True)
    # auto       = models.BooleanField(verbose_name=_('Автоперегортання слайдів'), default=True)
    # infinite   = models.BooleanField(verbose_name=_('"Нескінченний" слайдер'), default=True)
    # arrows     = models.BooleanField(verbose_name=_('Стрілки навігації (наступний / попередній)'), default=True)
    # navigation = models.BooleanField(verbose_name=_('Точки навігації слайдів'), default=True)
    # speed      = models.PositiveIntegerField(verbose_name=_('Швидкість зміни слайдів'), blank=True, null=True, default=6500, help_text=SPEED_HELP)

    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if self.page:
            Slide.objects.all().filter(slider=self).update(page=self.page)
        super().save(*args, **kwargs)


    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
        ]
        return fields

    class Meta:
        verbose_name = ('Слайдер')
        verbose_name_plural = ('Слайдери')
        ordering = ['order']


