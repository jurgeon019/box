
from admin_auto_filters.filters import AutocompleteFilter

class IsActiveFilter(AutocompleteFilter):
    title = 'статусу'
    field_name = 'checked'
