from django.contrib import admin 
from django.utils.html import mark_safe 
from modeltranslation.admin import TabbedTranslationAdmin
from .filters import IsActiveFilter


class ContactAdmin(admin.ModelAdmin):
    def show_link(self, obj):
        return mark_safe(f"<a href='{obj.url}'>{obj.url}</a>")

    def make_check_on(self, request, queryset):
        queryset.update(checked=True)

    def make_check_off(self, request, queryset):
        queryset.update(checked=False)

    make_check_on.short_description = ("Обробити")           
    make_check_off.short_description = ("Повернути до необроблених")           
    show_link.short_description = ("Ссилка")
    actions = [
        make_check_on,
        make_check_off,
    ]
    search_fields = [
        'name',
        'email',
        'phone',
        'message',
    ]
    list_filter = [
        # IsActiveFilter,
        'checked'
    ]
    list_display = [
        'name',
        'email',
        'phone',
        'message',
    ]
    exclude = [
        'url',
    ]
    readonly_fields = [
        'show_link'
    ]

from .models import Contact
admin.site.register(Contact, ContactAdmin)

# from box.apps.sw_blog.admin import PostCommentAdmin
# from box.apps.sw_shop.sw_catalog.admin import ItemReviewAdmin 
# from .models import ProxyComment, ProxyReview 
# admin.site.register(ProxyComment, PostCommentAdmin)
# admin.site.register(ProxyReview, ItemReviewAdmin)







