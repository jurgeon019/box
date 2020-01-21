from django.db import models
from django.urls import reverse 
from django.contrib.auth import get_user_model 


User = get_user_model()
class Member(models.Model):
    image          = models.ImageField(verbose_name=("Картинка"), blank=True, null=True)
    alt            = models.CharField(verbose_name=("Альт до картинки"), max_length=255, blank=True, null=True)
    meta_title     = models.TextField(verbose_name=("Мета Заголовок"), blank=True, null=True)
    meta_descr     = models.TextField(verbose_name=("Мета Опис"), blank=True, null=True)
    meta_key       = models.TextField(verbose_name=("Мета Ключові Слова"), blank=True, null=True)
    name           = models.CharField(verbose_name=("Імя"), max_length=255)
    description    = models.TextField(verbose_name=("Опис"), blank=True, null=True)
    specialization = models.CharField(verbose_name=("Спеціалізація"), blank=True, null=True, max_length=255)
    slug           = models.SlugField(verbose_name=("Ссилка"), unique=True, max_length=255)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("starway_member", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = ("Член")
        verbose_name_plural = ("Члени")
    


class CaseCategory(models.Model):
    image       = models.ImageField(verbose_name=("Картинка"), blank=True, null=True)
    alt         = models.CharField(verbose_name=("Альт до картинки"), max_length=255, blank=True, null=True)
    meta_title  = models.TextField(verbose_name=("Мета Заголовок"), blank=True, null=True)
    meta_descr  = models.TextField(verbose_name=("Мета Опис"), blank=True, null=True)
    meta_key    = models.TextField(verbose_name=("Мета Ключові Слова"), blank=True, null=True)
    title       = models.CharField(verbose_name=("Заголовок"), blank=True, null=True, max_length=255)
    description = models.TextField(verbose_name=("Опис"), blank=True, null=True)
    slug        = models.SlugField(verbose_name=("Ссилка"), unique=True, max_length=255)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("starway_case_category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = ("Категорія кейсу")
        verbose_name_plural = ("Категорії кейсу")
    


class Case(models.Model):
    image       = models.ImageField(verbose_name=("Картинка"), blank=True, null=True)
    alt         = models.CharField(verbose_name=("Альт до картинки"), max_length=255, blank=True, null=True)
    meta_title  = models.TextField(verbose_name=("Мета Заголовок"), blank=True, null=True)
    meta_descr  = models.TextField(verbose_name=("Мета Опис"), blank=True, null=True)
    meta_key    = models.TextField(verbose_name=("Мета Ключові Слова"), blank=True, null=True)
    title       = models.CharField(verbose_name=("Заголовок"), max_length=255, blank=True, null=True, help_text=(''))
    description = models.TextField(verbose_name=("Опис"), blank=True, null=True, help_text=('')) 
    slug        = models.SlugField(verbose_name=("Ссилка"), unique=True, max_length=255)
    category    = models.ForeignKey(verbose_name=("Категорія"), to="starway.CaseCategory", blank=True, null=True, on_delete=models.CASCADE, related_name="cases")

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("starway_case", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = ("Кейс")
        verbose_name_plural = ("Кейси")
    


class ServiceCategory(models.Model):
    image       = models.ImageField(verbose_name=("Картинка"), blank=True, null=True)
    alt         = models.CharField(verbose_name=("Альт до картинки"), max_length=255, blank=True, null=True)
    meta_title  = models.TextField(verbose_name=("Мета Заголовок"), blank=True, null=True)
    meta_descr  = models.TextField(verbose_name=("Мета Опис"), blank=True, null=True)
    meta_key    = models.TextField(verbose_name=("Мета Ключові Слова"), blank=True, null=True)
    title       = models.CharField(verbose_name=("Заголовок"), blank=True, null=True, max_length=255)
    description = models.TextField(verbose_name=("Опис"), blank=True, null=True)
    slug        = models.SlugField(verbose_name=("Ссилка"), unique=True, max_length=255)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("starway_service_category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = ("Категорія сервісу")
        verbose_name_plural = ("Категорії сервісу")
    


class Service(models.Model):
    image       = models.ImageField(verbose_name=("Картинка"), blank=True, null=True)
    alt         = models.CharField(verbose_name=("Альт до картинки"), max_length=255, blank=True, null=True)
    meta_title  = models.TextField(verbose_name=("Мета Заголовок"), blank=True, null=True)
    meta_descr  = models.TextField(verbose_name=("Мета Опис"), blank=True, null=True)
    meta_key    = models.TextField(verbose_name=("Мета Ключові Слова"), blank=True, null=True)
    title       = models.CharField(verbose_name=("Заголовок"), max_length=255, blank=True, null=True, help_text=(''))
    description = models.TextField(verbose_name=("Опис"), blank=True, null=True, help_text=('')) 
    slug        = models.SlugField(verbose_name=("Ссилка"), unique=True, max_length=255)
    # category    = models.ForeignKey(verbose_name=(""), to="starway.ServiceCategory", blank=True, null=True, on_delete=models.CASCADE, related_name="services")
    parent      = models.ForeignKey(verbose_name=("Батьківська послуга"), to="self", blank=True, null=True, related_name='subservices', on_delete=models.SET_NULL)


    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("starway_service", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = ("Сервіс")
        verbose_name_plural = ("Сервіси")
    

class MemberRequest(models.Model):
    full_name = models.CharField(verbose_name=("Ім'я"), max_length=255, blank=True, null=True)
    email     = models.CharField(verbose_name=("Емайл"), max_length=255, blank=True, null=True)
    phone     = models.CharField(verbose_name=("Номер телефону"), max_length=255, blank=True, null=True)
    message   = models.TextField(verbose_name=("Повідомлення"), blank=True, null=True)
    
    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = ("Запрос на членство в команду")
        verbose_name_plural = ("Запроси на членство в команду")


class ServiceRequest(models.Model):
    full_name = models.CharField(verbose_name=("Ім'я"), max_length=255, blank=True, null=True)
    email     = models.CharField(verbose_name=("Емайл"), max_length=255, blank=True, null=True)
    phone     = models.CharField(verbose_name=("Номер телефону"), max_length=255, blank=True, null=True)
    message   = models.TextField(verbose_name=("Повідомлення"), blank=True, null=True)
    service   = models.ForeignKey(verbose_name=("Сервіс"), to="starway.Service", blank=True, null=True, related_name='requests', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = ("Запрос послуги")
        verbose_name_plural = ("Запроси послуги")



class StarwayProfile(models.Model):
    user = models.OneToOneField(verbose_name=("Користувач"), to=User, blank=True, null=True, related_name='starway_profile', on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = ("Профіль")
        verbose_name_plural = ("Профілі")


