from django.apps import apps
from django.contrib import admin
from django.conf import settings


dummy_admin = type('dummyadmin', (object,),
                   {
                       'search_fields': []
                   })()


class ListDisplayAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = ['__str__', ] + [field.name for field in model._meta.fields if field.name != 'id'
                                             and type(field).__name__ != 'TextField']
        super().__init__(model, admin_site)


class ListFilterAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_filter = [field.name for field in model._meta.fields if field.choices]
        super().__init__(model, admin_site)


class AutocompleteFieldsAdminMixin(object):
    def __init__(self, model, admin_site):
        self.autocomplete_fields = [field.name for field in model._meta.fields if
                                    field.is_relation and admin.site._registry.get(
                                        field.related_model, dummy_admin
                                    ).search_fields]
        self.raw_id_fields = [field.name for field in model._meta.fields if
                              field.is_relation and not admin.site._registry.get(field.related_model,
                                                                                 dummy_admin).search_fields]
        super().__init__(model, admin_site)


class SelectRelatedFieldsAdminMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        related_fields = [field.name for field in self.model._meta.fields if field.is_relation]
        if related_fields:
            qs = qs.select_related(*related_fields)
        return qs


class DateHierarchyAdminMixin(object):
    def __init__(self, model, admin_site):
        date_and_datetime_fields = [field.name for field in model._meta.fields if
                                    type(field).__name__ in ['DateField', 'DateTimeField']]
        self.date_hierarchy = date_and_datetime_fields[0] if len(date_and_datetime_fields) == 1 else None
        super().__init__(model, admin_site)


ADMIN_AUTOREGISTER_EXCLUDE = [model.lower() for model in getattr(settings, 'ADMIN_AUTOREGISTER_EXCLUDE', [
    'contenttypes.ContentType',
    'auth.Permission',
    'session.Session',
    'admin.LogEntry',
])]
ADMIN_AUTOREGISTER_EXCLUDE_INLINES = getattr(settings, 'ADMIN_AUTOREGISTER_EXCLUDE_INLINES', True)

inline_models = [item.model for sublist in [v.inlines for k, v in admin.site._registry.items() if len(v.inlines) > 0]
                 for item
                 in sublist] if ADMIN_AUTOREGISTER_EXCLUDE_INLINES else []

models = [model for model in apps.get_models()
          if '{app_label}.{model_name}'.format(app_label=model._meta.app_label,
                                               model_name=model._meta.model_name) not in ADMIN_AUTOREGISTER_EXCLUDE
          and model not in inline_models]

def register_all():
    for model in models:
        admin_class = type('AutoRegisteredAdmin',
                        (ListDisplayAdminMixin, ListFilterAdminMixin, AutocompleteFieldsAdminMixin,
                            SelectRelatedFieldsAdminMixin, DateHierarchyAdminMixin,
                            admin.ModelAdmin), 
                            {}
                        )
        try:
            admin.site.register(model, admin_class)
        except admin.sites.AlreadyRegistered:
            pass

register_all()

def unregister_all():
    models = [model for model in apps.get_models()]
    for model in models:
        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass



# https://stackoverflow.com/questions/9443863/register-every-table-class-from-an-app-in-the-django-admin-page
# https://hackernoon.com/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5
# https://technowhisp.com/auto-registering-models-in-django-admin/
# https://avilpage.com/2017/11/django-tricks-auto-register-models-admin.html




