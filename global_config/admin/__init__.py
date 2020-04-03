from .admin import * 

admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(NotificationConfig, NotificationConfigAdmin)
admin.site.register(CatalogueConfig, CatalogueConfigAdmin)
admin.site.register(DesignConfig, DesignConfigAdmin)
# admin.site.register(Translation, TranslationAdmin)
admin.site.register(Robots, RobotsAdmin)
admin.site.register(Seo, SeoAdmin)

