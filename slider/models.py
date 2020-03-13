from django.db import models 
from django.conf import settings 


class ActiveManager(models.Manager):
    def all(self):
        return super().get_queryset().filter(is_active=True)


class Slide(models.Model):
    DISPLAY_CHOICES = (
        ("no_text", "Зображенні без тексту"),
        ("text_toned", "Текст на зображенні з тонуванням"),
        ("text_right", "Текст праворуч, зображення зліва"),
        ("text_left", "Текст зліва, зображення праворуч"),
    )
    slider    = models.ForeignKey(verbose_name=("Група слайдерів"), to='slider.Slider', related_name='images', on_delete=models.SET_NULL, null=True, blank=True) 
    page      = models.ForeignKey(verbose_name=("Сторінки"), to="page.Page", related_name="slides", on_delete=models.SET_NULL, blank=True, null=True)
    name      = models.CharField(verbose_name=("Назва"), max_length=255, blank=True, null=True)  
    image     = models.ImageField(verbose_name=("Зображення"), blank=False, null=False)
    alt       = models.CharField(verbose_name=("Назва зображення(alt)"), max_length=255, blank=True, null=True) 
    title     = models.CharField(verbose_name=("Вспливаюча підказка(title)"), max_length=255, blank=True, null=True)  
    text      = models.TextField(verbose_name=("Текст"), blank=True, null=True)  
    is_active = models.BooleanField(verbose_name=("Активність"), default=True)
    objects   = ActiveManager

    # TODO: настройки для лобецького
    # display   = models.CharField(verbose_name=("Варіант відображення"), choices=DISPLAY_CHOICES, max_length=255, default=0)  
    # mw_desc   = models.IntegerField(verbose_name=("Максимальна ширина дексктопі"), default=1050)  
    # mh_desc   = models.IntegerField(verbose_name=("Максимальна висота на дексктопі"), default=400)  
    # mw_mob    = models.IntegerField(verbose_name=("Максимальна ширина мобілках"), default=500)  
    # mh_mob    = models.IntegerField(verbose_name=("Максимальна висота на мобілках"), default=320)  


    def __str__(self):
        return f'{self.id}'
    
    def save(self, *args, **kwargs):
        if not self.page:
            if self.slider.page:
                self.page = self.slider.page 
        super().save(*args, **kwargs)
    
    def get_image_url(self):
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
    



class Slider(models.Model):

    name      = models.CharField(verbose_name=("Назва"), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=("Активність"), default=True)
    objects   = ActiveManager

    page = models.ForeignKey(
        verbose_name=("Сторінка"), 
        to="page.Page", 
        related_name='sliders', 
        blank=True,
        null=True, 
        on_delete=models.SET_NULL,
    )

    category = models.ForeignKey(
        verbose_name=("Категорія"), 
        to="item.ItemCategory", 
        related_name='sliders', 
        blank=True,
        null=True, 
        on_delete=models.SET_NULL,
    )

    brand = models.ForeignKey(
        verbose_name=("Бренд"), 
        to="item.ItemBrand", 
        related_name='sliders', 
        blank=True,
        null=True, 
        on_delete=models.SET_NULL,
    )

    item = models.ForeignKey(
        verbose_name=("Товар"), 
        to="item.Item", 
        related_name='sliders', 
        blank=True,
        null=True, 
        on_delete=models.SET_NULL,
    )
    
    # TODO: відображення на сторінках
    # pages          = models.ManyToManyField(verbose_name=("Сторінки"), to="page.Page", related_name='sliders', blank=True)
    # categories     = models.ManyToManyField(verbose_name=("Категорії"), to="item.ItemCategory", related_name='sliders', blank=True)
    # brands         = models.ManyToManyField(verbose_name=("Бренди"), to="item.ItemBrand", related_name='sliders', blank=True)
    # items          = models.ManyToManyField(verbose_name=("Товари"), to="item.Item", related_name='sliders', blank=True)
    
    # all_pages      = models.BooleanField(verbose_name=("Відображати групу на всіх сторінках"), default=False)
    # all_categories = models.BooleanField(verbose_name=("Відображати групу на всіх категоріях"), default=False)
    # all_brands     = models.BooleanField(verbose_name=("Відображати групу на всіх брендах"), default=False)
    # all_items      = models.BooleanField(verbose_name=("Відображати групу на всіх товарах"), default=False)
    # TODO: розібратись шо таке шорткод
    code          = models.SlugField(verbose_name=("id групи банера"), max_length=255, blank=True, null=True)
    shortcode     = models.SlugField(verbose_name=("Назва шорткода"), max_length=255, blank=True, null=True)
    is_individual = models.BooleanField(verbose_name=("Індивідуальний шорткод"), blank=True, null=True)
    # TODO: настройки для лобецького
    SPEED_HELP = ("Застосовується при включеному автоперелистуванні слайдів. Вказується в мілісекундах.")
    as_slider  = models.BooleanField(verbose_name=('Група банерів як слайдер'), default=True)
    auto       = models.BooleanField(verbose_name=('Автоперегортання слайдів'), default=True)
    infinite   = models.BooleanField(verbose_name=('"Нескінченний" слайдер'), default=True)
    arrows     = models.BooleanField(verbose_name=('Стрілки навігації (наступний / попередній)'), default=True)
    navigation = models.BooleanField(verbose_name=('Точки навігації слайдів'), default=True)
    speed      = models.PositiveIntegerField(verbose_name=('Швидкість зміни слайдів'), blank=True, null=True, default=6500, help_text=SPEED_HELP)


    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if self.page:
            Slide.objects.all().filter(slider=self).update(page=self.page)
        super().save(*args, **kwargs)


    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            # 'name',
        ]
        return fields

    class Meta:
        verbose_name = ('Слайдер')
        verbose_name_plural = ('Слайдери')
