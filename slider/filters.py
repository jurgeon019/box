from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from admin_auto_filters.filters import AutocompleteFilter 



class SliderFilter(AutocompleteFilter):
    title = 'слайдерами'
    field_name = 'slider'




