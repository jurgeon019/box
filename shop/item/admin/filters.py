
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from admin_auto_filters.filters import AutocompleteFilter

class CategoryFilter(AutocompleteFilter):
    title = 'категорією' 
    field_name = 'category' 

class MarkersFilter(AutocompleteFilter):
    title = 'маркерами' 
    field_name = 'markers' 

class BrandFilter(AutocompleteFilter):
    title = 'брендами'
    field_name = 'brand' 


class ItemStockFilter(AutocompleteFilter):
    title = 'наявністю'
    field_name = 'in_stock'


class ItemIsActiveFilter(AutocompleteFilter):
    title = 'активністю'
    field_name = 'is_active'

    
class ItemCategoryTreeRelatedFieldListFilter(TreeRelatedFieldListFilter):
    mptt_level_indent = 20



