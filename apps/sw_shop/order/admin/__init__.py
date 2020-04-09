from .admin import * 


admin.site.register(Order, OrderAdmin)
admin.site.register(ItemRequest, ItemRequestAdmin)
admin.site.register(OrderConfig, OrderConfigAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(OrderTag, OrderTagAdmin)
