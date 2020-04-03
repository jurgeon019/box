from django.db import models 
from django.utils.translation import gettext_lazy as _
from box.solo.models import SingletonModel


# class ImportLog(SingletonModel):
class ImportLog(models.Model):
    item   = models.ForeignKey(verbose_name=_("Товаp"), related_name='import_logs', to='item.Item', on_delete=models.CASCADE)
    status = models.CharField(verbose_name=_("Статус"), max_length=255)
    def __str__(self):
        return f'{self.item}' 
    class Meta:
        verbose_name        = _('Журнал імпорту')
        verbose_name_plural = verbose_name


class Import(models.Model):
    class Meta:
        verbose_name = _("Імпорт")
        verbose_name_plural = verbose_name


class Export(models.Model):
    class Meta:
        verbose_name = _("Експорт")
        verbose_name_plural = verbose_name





