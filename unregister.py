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
admin.site.unregister(get_user_model(), BoxUserAdmin)

from box.blog.admin import (
    Post, PostAdmin,
    PostCategory, PostCategoryAdmin,
    PostComment, PostCommentAdmin,
)
admin.site.unregister(Post, PostAdmin)
admin.site.unregister(PostCategory, PostCategoryAdmin)
admin.site.unregister(PostComment, PostCommentAdmin)


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
admin.site.unregister(ItemCurrency, ItemCurrencyAdmin)
admin.site.unregister(ItemStock, ItemStockAdmin)
admin.site.unregister(ItemCategory, ItemCategoryAdmin)
admin.site.unregister(ItemCurrencyRatio, ItemCurrencyRatioAdmin)
admin.site.unregister(ItemFeatureName, ItemFeatureNameAdmin)
admin.site.unregister(Item, ItemAdmin)
admin.site.unregister(ItemImage, ItemImageAdmin)
admin.site.unregister(ItemMarker, ItemMarkerAdmin)
admin.site.unregister(ItemBrand, ItemBrandAdmin)
admin.site.unregister(ItemReview, ItemReviewAdmin)
admin.site.unregister(ItemFeature, ItemFeatureAdmin)
admin.site.unregister(ItemFeatureValue, ItemFeatureValueAdmin)



from box.shop.cart.admin import (
    Cart, CartAdmin, 
    CartItem, CartItemAdmin
)
from box.shop.customer.admin import (
    Customer, CustomerAdmin,
)
admin.site.unregister(Customer, CustomerAdmin)
from box.shop.order.admin import (
    Status, StatusAdmin,
    Order, OrderAdmin,
    ItemRequest, ItemRequestAdmin,
    OrderConfig, OrderConfigAdmin,
    OrderTag, OrderTagAdmin,
)
admin.site.unregister(Order, OrderAdmin)
admin.site.unregister(ItemRequest, ItemRequestAdmin)
admin.site.unregister(OrderConfig, OrderConfigAdmin)
admin.site.unregister(Status, StatusAdmin)
admin.site.unregister(OrderTag, OrderTagAdmin)

from box.shop.liqpay.admin import (
    Payment, PaymentAdmin,
)
from box.content.admin import (
    Page, PageAdmin,
    Text, TextAdmin,
)
admin.site.unregister(Page, PageAdmin)
admin.site.unregister(Text, TextAdmin)
from box.global_config.admin import (
    SiteConfig, SiteConfigAdmin,
    NotificationConfig, NotificationConfigAdmin,
    CatalogueConfig, CatalogueConfigAdmin,
)
admin.site.unregister(SiteConfig, SiteConfigAdmin)
admin.site.unregister(NotificationConfig, NotificationConfigAdmin)
admin.site.unregister(CatalogueConfig, CatalogueConfigAdmin)


from box.seo.admin import (
    Robots, RobotsAdmin,
    Seo, SeoAdmin,
    ItemSeo, ItemSeoAdmin,
)
admin.site.unregister(Robots, RobotsAdmin)
admin.site.unregister(Seo, SeoAdmin)
admin.site.unregister(ItemSeo, ItemSeoAdmin)


from box.faq.admin import (
    Faq, FaqAdmin,
)
admin.site.unregister(Faq, FaqAdmin)

from box.content.admin import (
    Slide, SlideAdmin,
    Slider, SliderAdmin,
)
admin.site.unregister(Slider, SliderAdmin)
admin.site.unregister(Slide, SlideAdmin)

from box.imp_exp.admin import (
    ImportLog, ImportLogAdmin
)
admin.site.unregister(ImportLog, ImportLogAdmin)

from box.design.admin import (
    DesignConfig, DesignConfigAdmin,
    # Translation, TranslationAdmin,
)
admin.site.unregister(DesignConfig, DesignConfigAdmin)
# admin.site.unregister(Translation, TranslationAdmin)





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
admin_plus.unregister(Redirect)
admin_plus.unregister(Site)
admin_plus.unregister(User, UserAdmin)
admin_plus.unregister(Group, GroupAdmin)
admin_plus.unregister(Cart, CartAdmin)
admin_plus.unregister(CartItem, CartItemAdmin)
