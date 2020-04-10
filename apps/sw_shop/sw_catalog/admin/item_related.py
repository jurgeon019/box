from .imports import * 
import nested_admin 


class ItemImageAdmin(
    # nested_admin.NestedTabularInline,
    BaseAdmin, SortableAdminMixin,
    ):
    # def get_model_perms(self, request):
    #     return {}

    def show_item(self, obj):
        return show_admin_link(obj=obj, obj_attr='item', obj_name='title')

    show_item.short_description = ('Товар')
    
    list_display = [
        'id',
        'show_image',
        'alt',
        'show_item',
    ]
    list_display_links = [
        'id',
        'alt',
    ]
    list_editable = []
    autocomplete_fields = [
        'item',
    ]


class ItemCurrencyAdmin(
    ImportExportModelAdmin,
    ImportExportActionModelAdmin,
    TabbedTranslationAdmin,
    ):
    resource_class = ItemCurrencyResource
    actions = [
        'delete',
    ]
    list_filter = []
    list_display = [
        'name',
        'code',
        'rate',
        'is_main',
    ]
    list_display_links = [
        'name',
        'code',
    ]
    list_editable = [
        'rate',
    ]
    readonly_fields = [
        # 'is_active',
        'is_main',
        # 'updated',
        # 'created',
        # 'code',
    ]
    formfield_overrides = {
        # models.CharField: {'widget': TextInput(attrs={'size':8})},
        # models.DecimalField: {'widget': NumberInput(attrs={"style":"width:70px"})}
    }
    search_fields = [
        'name',
        'code',
    ]


class ItemCurrencyRatioAdmin(admin.ModelAdmin):
    list_display_links = [
        'id',
        'main',
        'compared',
        'ratio',
    ]
    list_display = [
        'id',
        'main',
        'compared',
        'ratio',
    ]


class ItemStockAdmin(TabbedTranslationAdmin):
    def get_model_perms(self, request):
        return {}

    list_display = [
        'id',
        'text',
        'availability',
        'colour',
    ] 
    list_display_links = [
        'id',
        'text',

    ] 
    list_editable = [
        'availability',
    ]
    search_fields = [
        'text',
    ]


class ItemMarkerAdmin(TabbedTranslationAdmin):
    # def get_model_perms(self, request):
    #     return {}
    search_fields = [
        'text',
    ]
    fields = [
        'text',
    ]


class ItemBrandAdmin(BaseAdmin, SortableAdminMixin, TabbedTranslationAdmin):
    # change_form
    fieldsets = [
        base_main_info,
        seo,
    ]
    prepopulated_fields = {
        'slug':('title',)
    }


class ItemReviewAdmin(
    BaseAdmin,
    # nested_admin.NestedTabularInline,
    ):
    list_display = [
        'id',
        'text',
        'phone',
        'email',
        'name',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'text',
        'phone',
        'email',
        'name',
    ]


