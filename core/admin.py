from django.contrib import admin
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model 
from django.contrib.auth.admin import (
    User, UserAdmin,
    Group, GroupAdmin,
)
from box.custom_auth.admin import (
   BoxUserAdmin,
)
admin.site.register(get_user_model(), BoxUserAdmin)

from box.blog.admin import (
    Post, PostAdmin,
    PostCategory, PostCategoryAdmin,
    PostComment, PostCommentAdmin,
)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(PostComment, PostCommentAdmin)


from box.shop.item.admin import (
    Item, ItemAdmin,
    ItemCategory, ItemCategoryAdmin,
    ItemCurrency, ItemCurrencyAdmin,
    ItemCurrencyRatio, ItemCurrencyRatioAdmin,
    ItemStock, ItemStockAdmin, 
    ItemFeatureName, ItemFeatureNameAdmin,
    ItemMarker, ItemMarkerAdmin,
    ItemBrand, ItemBrandAdmin,
    ItemImage, ItemImageAdmin,
    ItemReview, ItemReviewAdmin,
    ItemFeature, ItemFeatureAdmin,
    ItemFeatureValue, ItemFeatureValueAdmin,
)
admin.site.register(ItemCurrency, ItemCurrencyAdmin)
admin.site.register(ItemStock, ItemStockAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(ItemCurrencyRatio, ItemCurrencyRatioAdmin)
admin.site.register(ItemFeatureName, ItemFeatureNameAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage, ItemImageAdmin)
admin.site.register(ItemMarker, ItemMarkerAdmin)
admin.site.register(ItemBrand, ItemBrandAdmin)
admin.site.register(ItemReview, ItemReviewAdmin)
admin.site.register(ItemFeature, ItemFeatureAdmin)
admin.site.register(ItemFeatureValue, ItemFeatureValueAdmin)



from box.shop.cart.admin import (
    Cart, CartAdmin, 
    CartItem, CartItemAdmin
)
from box.shop.customer.admin import (
    Customer, CustomerAdmin,
)
admin.site.register(Customer, CustomerAdmin)
from box.shop.order.admin import (
    Status, StatusAdmin,
    Order, OrderAdmin,
    ItemRequest, ItemRequestAdmin,
    OrderConfig, OrderConfigAdmin,
    OrderTag, OrderTagAdmin,
)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemRequest, ItemRequestAdmin)
admin.site.register(OrderConfig, OrderConfigAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(OrderTag, OrderTagAdmin)

from box.shop.liqpay.admin import (
    Payment, PaymentAdmin,
)
from box.page.admin import (
    Page, PageAdmin,
    Text, TextAdmin,
)
admin.site.register(Page, PageAdmin)
admin.site.register(Text, TextAdmin)
from box.global_config.admin import (
    SiteConfig, SiteConfigAdmin,
    NotificationConfig, NotificationConfigAdmin,
    CatalogueConfig, CatalogueConfigAdmin,
)
admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(NotificationConfig, NotificationConfigAdmin)
admin.site.register(CatalogueConfig, CatalogueConfigAdmin)


from box.seo.admin import (
    Robots, RobotsAdmin,
    Seo, SeoAdmin,
    ItemSeo, ItemSeoAdmin,
)
admin.site.register(Robots, RobotsAdmin)
admin.site.register(Seo, SeoAdmin)
admin.site.register(ItemSeo, ItemSeoAdmin)


from box.faq.admin import (
    Faq, FaqAdmin,
)
admin.site.register(Faq, FaqAdmin)

from box.slider.admin import (
    Slide, SlideAdmin,
    Slider, SliderAdmin,
)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Slide, SlideAdmin)

from box.imp_exp.admin import (
    ImportLog, ImportLogAdmin
)
admin.site.register(ImportLog, ImportLogAdmin)

from box.design.admin import (
    DesignConfig, DesignConfigAdmin,
    # Translation, TranslationAdmin,
)
admin.site.register(DesignConfig, DesignConfigAdmin)
# admin.site.register(Translation, TranslationAdmin)





####################################################
# unregister zone 

admin.site.unregister(Redirect)
admin.site.unregister(Site)
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








####################################################
# admin plus zone 



class AdminPlus(admin.AdminSite):
    site_header = "Site Admin"
    site_title  = "Site Admin"
    index_title = "Site Admin"


admin_plus = AdminPlus(name='admin_plus')
admin_plus.register(Redirect)
admin_plus.register(Site)
admin_plus.register(User, UserAdmin)
admin_plus.register(Group, GroupAdmin)
admin_plus.register(Cart, CartAdmin)
admin_plus.register(CartItem, CartItemAdmin)
