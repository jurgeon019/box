from .admin import * 



admin.site.register(get_user_model(), BoxUserAdmin)
admin.site.register(User, UserAdmin)
# admin.site.register(Group, GroupAdmin)
