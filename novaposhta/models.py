from django.db import models
from django.utils.translation import ugettext_lazy as _


class Warehouse(models.Model):
    title = models.CharField(_('Title'), max_length=255, db_index=True)
    address = models.CharField(_('Address'), max_length=255, db_index=True)

    @property
    def full_name(self):
        return '{}, {}'.format(self.title, self.address)

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'title',
            'address',
        ]
        return fields

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')


class Area(models.Model):
    title = models.CharField(_('Title'), max_length=255, db_index=True)

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'title',
        ]
        return fields

    class Meta:
        verbose_name = _('Область')
        verbose_name_plural = _('Області')



class Region(models.Model):
    title = models.CharField(_('Title'), max_length=255, db_index=True)
    area  = models.ForeignKey(verbose_name=_("Area"),   to='novaposhta.Area', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title} -> {self.area.title}'

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'title',
        ]
        return fields
    class Meta:
        verbose_name = _('район')
        verbose_name_plural = _('райони')


class Type(models.Model):
    title = models.CharField(_('Title'), max_length=255, db_index=True)
    def __str__(self):
        return f'{self.title}'

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'title',
        ]
        return fields
    
    class Meta:
        verbose_name = _('Тип населеного пункту')
        verbose_name_plural = _('Типи населених пунктів')


class Settlement(models.Model):
    title     = models.CharField(verbose_name=_('Title'),     max_length=255, db_index=True)
    type      = models.CharField(verbose_name=_("Type"),      max_length=255)
    latitude  = models.CharField(verbose_name=_("latitude"),  max_length=255)
    longitude = models.CharField(verbose_name=_("longitude"), max_length=255)
    region    = models.ForeignKey(verbose_name=_("Region"), to='novaposhta.Region', on_delete=models.SET_NULL, null=True)

    @property
    def area(self):
        area = ''
        if self.region:
            area = self.region.area 
        return area 

    def __str__(self):
        return f'{self.title} -> {self.region}'

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'title',
            'type',
        ]
        return fields

    class Meta:
        verbose_name = _('населений пункт')
        verbose_name_plural = _('населені пункти')



