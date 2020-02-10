from django.contrib import admin
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.contrib.auth.models import (User, Group,)
from django.contrib.auth.admin import (UserAdmin, GroupAdmin,)


class CustomAdmin(admin.AdminSite):
    site_header = "Site Admin"
    site_title  = "Site Admin"
    index_title = "Site Admin"


custom_admin = CustomAdmin(name='custom_admin')


class AdminPlus(admin.AdminSite):
    site_header = "Site Admin"
    site_title  = "Site Admin"
    index_title = "Site Admin"


admin_plus = AdminPlus(name='admin_plus')
admin_plus.register(Redirect)
admin_plus.register(Site)
admin_plus.register(User, UserAdmin)
admin_plus.register(Group, GroupAdmin)



from box.blog.admin import * 
from box.shop.item.admin import * 
from box.shop.cart.admin import * 
from box.shop.profile.admin import * 
from box.shop.order.admin import * 
from box.shop.liqpay.admin import * 

from box.pages.admin import * 
from box.custom_auth.admin import *
from box.custom_admin.admin import * 

from box.custom_auth.models import User

admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(CurrencyRatio, CurrencyRatioAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Page, PageAdmin)

# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem, CartItemAdmin)








from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
admin.site.unregister(Redirect)
admin.site.unregister(Site)

from django.contrib.auth.models import (User, Group,)
admin.site.unregister(Group)


try:
    from django_celery_beat.models import *
    admin.site.unregister(IntervalSchedule)
    admin.site.unregister(CrontabSchedule)
    admin.site.unregister(SolarSchedule)
    admin.site.unregister(ClockedSchedule)
    admin.site.unregister(PeriodicTask)
except: 
    pass 




try:
    from filebrowser.models import * 
    admin.site.unregister(FileBrowser)
except: 
    pass



try:
    from allauth.account.models import * 
    # admin.site.unregister(EmailConfirmation)
    admin.site.unregister(EmailAddress)
except: 
    pass 



try:
    from django.contrib.flatpages.models import *
    admin.site.unregister(FlatPage)
except: 
    pass 




try:
    from allauth.socialaccount.models import * 
    admin.site.unregister(SocialApp)
    admin.site.unregister(SocialToken)
    admin.site.unregister(SocialAccount)
except: 
    pass



