from django.db import models 
from box.solo.models import SingletonModel
from tinymce import HTMLField
from tinymce.widgets import TinyMCE
from colorfield.fields import ColorField
# Template
# TemplateFile
# TemplateStyle
# TemplateScript
# SiteImage
# SiteTranslation

from box.page.models import PageFeature


# class Translation(PageFeature):
#     class Meta:
#         proxy = True 


class DesignConfig(SingletonModel):
    logo     = models.ImageField(verbose_name=("Логотип сайту"), blank=True, null=True, help_text=("Допустимі розширення зображень png, gif, jpg, jpeg, ico"), default='')
    favicon  = models.ImageField(verbose_name=("Фавікон сайту"), blank=True, null=True, help_text=("Допустимі розширення зображень png, gif, jpg, jpeg, ico"), default='') 
    delivery = HTMLField(verbose_name=("Способи доставки(в картці товару)"), blank=True, null=True, )
    payment  = HTMLField(verbose_name=("Способи оплати(в картці товару)"), blank=True, null=True, )
    email    = models.CharField(verbose_name=("Е-mail"), max_length=255, blank=True, null=True, )
    phones   = models.CharField(verbose_name=("Телефони(через кому)"), max_length=255, blank=True, null=True, )
    map      = models.TextField(verbose_name=("Мапа в контактах"), blank=True, null=True, help_text=("Необхідно вставити код з Google maps або Яндекс карти"))
    time     = HTMLField(verbose_name=("Чаc роботи"), null=True, blank=True, )
    social   = models.TextField(verbose_name=("Посилання на соц.мережі в футері (з нового рядка)"), blank=True, null=True)



    colour_buttons                = ColorField(verbose_name=("Колір кнопок"), blank=True, null=True)
    colour_buttons_text           = ColorField(verbose_name=("Колір тексту на кнопках"), blank=True, null=True)
    colour_buttons_hover          = ColorField(verbose_name=("Колір кнопок по наведенню"), blank=True, null=True)
    colour_buttons_text_hover     = ColorField(verbose_name=("Колір тексту на кнопках по наведенню"), blank=True, null=True)
    colour_main                   = ColorField(verbose_name=("Основний корпоративний колір"), blank=True, null=True)
    colour_additional             = ColorField(verbose_name=("Додатковий корпоративний колір"), blank=True, null=True)
    colour_main_background        = ColorField(verbose_name=("Колір тексту на основному корпоративному фоні"), blank=True, null=True)
    colour_additional_background  = ColorField(verbose_name=("Колір тексту на додатковому корпоративному фоні"), blank=True, null=True)
    colour_background             = ColorField(verbose_name=("Колір фону сайту"), blank=True, null=True)

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'logo',
            'delivery',
            'payment',
            'time',
        ]
        return fields

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Налаштування дизайну'
        verbose_name_plural = 'Налаштування дизайну'



class DesignAdvantage(models.Model):
    config      = models.ForeignKey(verbose_name=("Конфіг"), to="design.DesignConfig", related_name="advantages", on_delete=models.CASCADE)
    image       = models.ImageField(verbose_name=("Зображення"), blank=True, null=True)
    alt         = models.CharField(verbose_name=("альт"), blank=True, null=True, max_length=255)
    description = models.TextField(verbose_name=("Опис"))
    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'alt',
            'description',
        ]
        return fields
    def __str__(self):
        return f"{self.image}"

    class Meta:
        verbose_name = 'Перевага' 
        verbose_name_plural = 'Переваги' 


