from .imports import * 
from django.utils.translation import gettext_lazy as _



from box.core.utils import *
# from box.core.utils import ImportExportClonableMixin

class ItemCategoryAdmin(
    BaseMixin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin, 
    DraggableMPTTAdmin,
    ClonableModelAdmin, 
    admin.ModelAdmin,
    ):
    # changelist
    def tree_title(self, obj):
        lvl = obj._mpttfield('level') * self.mptt_level_indent
        return mark_safe(f'<div style="text-indent:{lvl}px">{obj.tree_title}</div>')
    
    tree_title.short_description = _('Заголовок')
    expand_tree_by_default = False 
    mptt_level_indent = 20
    resource_class = ItemCategoryResource
    inlines = [
        ItemCategoryInline,
    ]
    actions = [
        "is_active_on",
        "is_active_off",
    ]
    mptt_indent_field = "currency"
    list_display = [
        'slug',
        'code',
        'tree_actions',
        "show_image",
        # 'indented_title',
        'tree_title',
        'is_active',
        'show_site_link',
        'show_delete_link',
    ]
    search_fields = [
        'title',
    ]
    list_display_links = [
        # 'indented_title',
        'tree_title',
    ]
    list_editable = [
        'is_active',
    ]
    list_filter = (
        # ('title', TreeRelatedFieldListFilter),
    )
    list_per_page = 200 

    # changeform
    formfield_overrides = {
        models.ImageField:{'widget': AdminImageWidget},
        models.CharField: {'widget': NumberInput(attrs={'size':'40'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }
    prepopulated_fields = {
        "slug": ("title",),
    }
    fieldsets = [
        [_('ОСНОВНА ІНФОРМАЦІЯ'), {
            "fields":[
                "title",
                'is_active',
                "currency",
                "image",
                'parent',
                'description',
                "created",
                'updated',
            ]
        }],
        seo,
    ]
    autocomplete_fields = [
        'parent',
    ]
    
   
