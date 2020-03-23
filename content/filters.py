from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _




class TextIsNoneFilter(SimpleListFilter):
    title = 'значенням'
    parameter_name = 'value'

    def lookups(self, request, model_admin):
        return [ 
            ('full', _('Є текст')),
            ('null', _("Немає тексту")),
        ]
    def queryset(self, request, queryset):
        if self.value == 'full':
            return queryset.distinct().filter(value__isnull=False)
        elif self.value() == 'null':
            return queryset.distinct().filter(value__isnull=True)
        



