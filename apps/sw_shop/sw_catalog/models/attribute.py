from django.db import models 
from django.utils.translation import gettext_lazy as _


class AttributeCategory(models.Model):
    name   = models.CharField(
        verbose_name=_("Назва"), max_length=255, unique=True
    )
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('категорія атрибутів')
        verbose_name_plural = _('категорії атрибутів')

    @classmethod
    def modeltranslation_fields(cls):
        return ['name']


class Attribute(models.Model):
    code = models.SlugField(
        verbose_name=_("Код"), max_length=255, unique=True, blank=True, null=True
    )
    name = models.CharField(
        verbose_name=_("Назва"), max_length=50, 
    )
    category = models.ForeignKey(
        verbose_name=_("Категорія"), to="sw_catalog.AttributeCategory", 
        related_name="attributes", on_delete=models.SET_NULL, 
        blank=True, null=True,
    )

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('атрибут')
        verbose_name_plural = _('атрибути')
        unique_together = [
            'name',
            'category',
        ]
    
    @classmethod
    def modeltranslation_fields(cls):
        return ['name']


class AttributeValue(models.Model):
    code = models.SlugField(
        verbose_name=_("Код"), max_length=255, unique=True, 
        blank=True, null=True,
    )
    attribute = models.ForeignKey(
        verbose_name=_("Атрибут"), to="sw_catalog.Attribute", 
        on_delete=models.SET_NULL, blank=True, null=True,
    )
    value = models.CharField(
        verbose_name=_("Значення"), max_length=255, unique=True,
    )

    def __str__(self):
        return f'{self.value}'
    
    def save(self, *args, **kwargs):
        if self.value:
            self.value = self.value.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('значення атрибуту')
        verbose_name_plural = _('значення атрибутів')

    @classmethod
    def modeltranslation_fields(cls):
        return ['value']


class ItemAttribute(models.Model):
    item = models.ForeignKey(
        verbose_name=_("Товар"), to="sw_catalog.Item", 
        on_delete=models.CASCADE, related_name='item_attributes',
    )
    attribute = models.ForeignKey(
        verbose_name=_("Атрибут"), to='sw_catalog.Attribute', 
        on_delete=models.CASCADE,
    )
    is_option = models.BooleanField(
        verbose_name=_("Опція?"), default=False
    )

    @property
    def has_multiple_values(self):
        return self.values.all().count() > 1

    def __str__(self):
        return f'{self.attribute.name}'

    class Meta:
        verbose_name = _("атрибут товару")
        verbose_name_plural = _("атрибути товарів")
        unique_together = [
            'item',
            'attribute',
        ]


class ItemAttributeValue(models.Model):
    item_attribute = models.ForeignKey(
        to="sw_catalog.ItemAttribute", verbose_name=_("Атрибут товару"), on_delete=models.CASCADE,
        related_name='variants',
    )
    value = models.ForeignKey(
        verbose_name=_("Значення"), 
        to='sw_catalog.AttributeValue', 
        on_delete=models.CASCADE,
        # unique=True,
    )
    price = models.DecimalField(
        verbose_name=_("Ціна"), max_digits=9, decimal_places=2, default=0,
    )
    description = models.TextField(
        verbose_name=_("Опис"), blank=True, null=True, 
    )

    @classmethod
    def modeltranslation_fields(self):
        return ['description',]

    def __str__(self):
        return f'{self.value}'


    class Meta:
        verbose_name = _('значення атрибутів товарів')
        verbose_name_plural = _('значення атрибутів товарів')


