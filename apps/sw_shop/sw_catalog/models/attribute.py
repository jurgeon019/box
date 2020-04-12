from django.db import models 
from django.utils.translation import gettext_lazy as _




class AttributeCategory(models.Model):
    name   = models.CharField(
        verbose_name=_("Назва"), max_length=255, 
        unique=True, blank=True, null=True,
    )
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('категорія атрибутів')
        verbose_name_plural = _('категорії атрибутів')
    @classmethod
    def modeltranslation_fields(cls):
        return ['name']


class Attribute(models.Model):
    name = models.CharField(
        verbose_name=_("Назва"), max_length=50, #unique=True,
    )
    category = models.ForeignKey(
        verbose_name=_("Категорія"), to="sw_catalog.AttributeCategory", 
        related_name="attributes", on_delete=models.SET_NULL, 
        blank=True, null=True,
    )

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


class AttributeVariant(models.Model):
    value = models.ForeignKey(
        verbose_name=_("Значення"),
        to='sw_catalog.AttributeVariantValue', on_delete=models.CASCADE,
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
        abstract = True 
        verbose_name = _('варіант атрибутів')
        verbose_name_plural = _('варіанти атрибутів')


class AttributeVariantValue(models.Model):
    value = models.CharField(
        verbose_name=_("Значення"), max_length=50,
    )
    def __str__(self):
        return f'{self.value}'
    class Meta:
        verbose_name = _('значення варіантів атрибутів')
        verbose_name_plural = _('значення варіантів атрибутів')
    @classmethod
    def modeltranslation_fields(cls):
        return ['value']


class ObjAttribute(models.Model):
    is_option = models.BooleanField(
        verbose_name=_("Опція?"), default=False
    )
    attribute = models.ForeignKey(
        verbose_name=_("Атрибут"), to='sw_catalog.Attribute', 
        on_delete=models.CASCADE,
    )

    @property
    def has_multiple_values(self):
        return self.values.all().count() > 1

    def __str__(self):
        return f'{self.attribute.name}'

    class Meta:
        abstract = True 


# Item 


class ItemAttribute(ObjAttribute):
    item = models.ForeignKey(
        verbose_name=_("Товар"), to="sw_catalog.Item", 
        on_delete=models.CASCADE, related_name='item_attributes',
    )

    class Meta:
        verbose_name = _("атрибут товарів")
        verbose_name_plural = _("атрибути товарів")
        unique_together = [
            'item',
            'attribute',
        ]


class ItemAttributeVariant(AttributeVariant):
    item_attribute = models.ForeignKey(
        to="sw_catalog.ItemAttribute", verbose_name=_("Атрибут товару"), on_delete=models.CASCADE,
        related_name='variants',
    )

    class Meta:
        verbose_name = _('варіант значення атрибуту товару')
        verbose_name_plural = _('варіанти значеннь атрибутів товару')


# Item Category 

class ItemCategoryAttribute(ObjAttribute):
    # item_category = models.ForeignKey(
    #     verbose_name=_("Категорія"), to="sw_catalog.ItemCategory", 
    #     on_delete=models.CASCADE, related_name='item_category_attributes',
    # )
    item_categories = models.ManyToManyField(
        verbose_name=_("Категорія"), 
        to="sw_catalog.ItemCategory", 
        related_name='item_category_attributes',
    )
    variants = models.ManyToManyField(
        verbose_name=_("Варіанти атрибутів товарів"), 
        to="sw_catalog.ItemCategoryAttributeVariant", 
        related_name='item_category_attributes',
    )
    class Meta:
        verbose_name = _("атрибут категорій товарів")
        verbose_name_plural = _("атрибути категорій товарів")


class ItemCategoryAttributeVariant(AttributeVariant):
    class Meta:
        verbose_name = _('варіант атрибутів категорій товарів')
        verbose_name_plural = _('варіанти атрибутів категорій товарів')




