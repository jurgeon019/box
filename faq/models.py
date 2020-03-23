from django.db import models 
from django.shortcuts import reverse 
from adminsortable.models import SortableMixin
from box.core.models import BaseMixin
from django.utils.translation import gettext_lazy as _

class Faq(BaseMixin):
    name      = models.CharField(verbose_name=_("Назва"), max_length=255)
    answer    = models.TextField(verbose_name=_("Відповідь"))

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = ("FAQ")
        verbose_name_plural = ("FAQ")
        ordering = ['order']
    
    def get_absolute_url(self):
        try:
            return reverse("faq", kwargs={"pk": self.pk})
        except:
            return '' 
    
    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'name',
            'answer',
        ]
        return fields
