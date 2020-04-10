from django.db import models 
from django.utils.translation import gettext_lazy as _



# TODO: ItemCategoryAttribute, як на ельмасті


class AttributeCategory(models.Model):
    """
    Комплектуючі, Габарити, характеристики
    """

    name   = models.CharField(
        verbose_name=_("Назва"), max_length=255, 
        unique=True, blank=True, null=True,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('категорія атрибуту')
        verbose_name_plural = _('категорії атрибуту')
    
    @classmethod
    def modeltranslation_fields(cls):
        fields = [
            'name',
        ]
        return fields


class Attribute(models.Model):
    """
    Рама ,Вилка ,Амортизатор ,Переднє колесо
    Заднє колесо, Гальмівні диски, Гальма, Руль 
    Максимальна швидкість, Середній пробіг на одному заряді,  
    Час повного заряду батареї

    глобально у всьому магазині
    """

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
        fields = [
            'name',
        ]
        return fields


class ItemAttribute(models.Model):
    """
    Рама ,Вилка ,Амортизатор ,Переднє колесо
    Заднє колесо, Гальмівні диски, Гальма, Руль 
    Максимальна швидкість, Середній пробіг на одному заряді,  
    Час повного заряду батареї

    у конкретного товара
    """
    item = models.ForeignKey(
        verbose_name=_("Товар"), to="sw_catalog.Item", 
        on_delete=models.CASCADE,
    )
    attribute = models.ForeignKey(
        verbose_name=_("Назва"), to='sw_catalog.Attribute', 
        on_delete=models.CASCADE, related_name='attributes',
    )
    is_option = models.BooleanField(
        verbose_name=_("Опція"), default=False
    )

    @property
    def has_multiple_values(self):
        res = False 
        if self.values.all().count() > 1:
            res = True 
        return res

    # @property
    # def variants(self):
    #     return ItemAttributeVariant.objects.filter(item_attibute=self)

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def modeltranslation_fields(cls):
        fields = [
        ]
        return fields

    class Meta:
        verbose_name = _('атрибут товару')
        verbose_name_plural = _('атрибути товару')


class ItemAttributeVariant(models.Model):
    """
    чорний, Сірий, Хакі, Мото, Вело 

    конкретно для одного атрибуту
    """
    item_attribute = models.ForeignKey(
        to="sw_catalog.ItemAttribute", verbose_name=_("Атрибут товару"), on_delete=models.CASCADE,
        related_name='variants',
    )
    value = models.ForeignKey(
        to='sw_catalog.ItemAttributeVariantValue', on_delete=models.CASCADE,
    )
    # price = models.DecimalField(
    #     verbose_name=_("Ціна"), max_digits=5, decimal_places=2, default=0
    # )

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = _('варіант значення атрибуту товару')
        verbose_name_plural = _('варіанти значеннь атрибутів товару')


class ItemAttributeVariantValue(models.Model):
    """
    чорний, Сірий, Хакі, Мото, Вело 

    глобально для всіх атрибутів
    """
    value = models.CharField(
        verbose_name=_("Значення"), max_length=50,
    )
    price = models.DecimalField(
        verbose_name=_("Ціна"), max_digits=5, decimal_places=2, default=0
    )

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = _('значення атрибуту товару')
        verbose_name_plural = _('значення атрибутів товару')

    @classmethod
    def modeltranslation_fields(cls):
        fields = [
            'value',
        ]
        return fields

