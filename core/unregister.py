# from django.contrib import admin
# from django.contrib.redirects.models import Redirect
# from django.contrib.sites.models import Site
# from django.contrib.auth import get_user_model 
# from django.contrib.auth.admin import (
#     User, UserAdmin,
#     Group, GroupAdmin,
# )
# from box.sw_auth.admin import (
#    BoxUserAdmin,
# )
# # admin.site.unregister(get_user_model())

# from box.blog.admin import (
#     Post, PostAdmin,
#     PostCategory, PostCategoryAdmin,
#     PostComment, PostCommentAdmin,
# )
# admin.site.unregister(Post)
# admin.site.unregister(PostCategory)
# admin.site.unregister(PostComment)


# from box.sw_shop.item.admin import (
#     Item, ItemAdmin,
#     ItemCategory, ItemCategoryAdmin,
#     ItemCurrency, ItemCurrencyAdmin,
#     ItemCurrencyRatio, ItemCurrencyRatioAdmin,
#     ItemStock, ItemStockAdmin, 
#     ItemFeatureName, ItemFeatureNameAdmin,
#     ItemMarker, ItemMarkerAdmin,
#     ItemBrand, ItemBrandAdmin,
#     ItemImage, ItemImageAdmin,
#     ItemReview, ItemReviewAdmin,
#     ItemFeature, ItemFeatureAdmin,
#     ItemFeatureValue, ItemFeatureValueAdmin,
# )
# admin.site.unregister(ItemCurrency)
# admin.site.unregister(ItemStock)
# admin.site.unregister(ItemCategory)
# admin.site.unregister(ItemCurrencyRatio)
# admin.site.unregister(ItemFeatureName)
# admin.site.unregister(Item)
# admin.site.unregister(ItemImage)
# admin.site.unregister(ItemMarker)
# admin.site.unregister(ItemBrand)
# admin.site.unregister(ItemReview)
# admin.site.unregister(ItemFeature)
# admin.site.unregister(ItemFeatureValue)



# from box.sw_shop.cart.admin import (
#     Cart, CartAdmin, 
#     CartItem, CartItemAdmin
# )
# from box.sw_shop.customer.admin import (
#     Customer, CustomerAdmin,
# )
# admin.site.unregister(Customer)
# from box.sw_shop.order.admin import (
#     Status, StatusAdmin,
#     Order, OrderAdmin,
#     ItemRequest, ItemRequestAdmin,
#     OrderConfig, OrderConfigAdmin,
#     OrderTag, OrderTagAdmin,
# )
# admin.site.unregister(Order)
# admin.site.unregister(ItemRequest)
# admin.site.unregister(OrderConfig)
# admin.site.unregister(Status)
# admin.site.unregister(OrderTag)

# from box.payment.liqpay.admin import (
#     Payment, PaymentAdmin,
# )
# from box.content.admin import (
#     Page,   PageAdmin,
#     Text,   TextAdmin,
#     Slide,  SlideAdmin,
#     Slider, SliderAdmin,
#     Faq,    FaqAdmin,
# )
# admin.site.unregister(Page)
# admin.site.unregister(Text)
# admin.site.unregister(Slider)
# admin.site.unregister(Slide)
# admin.site.unregister(Faq)

# from box.global_config.admin import (
#     SiteConfig, SiteConfigAdmin,
#     NotificationConfig, NotificationConfigAdmin,
#     CatalogueConfig, CatalogueConfigAdmin,
#     DesignConfig, DesignConfigAdmin,
#     # Translation, TranslationAdmin,
#     Robots, RobotsAdmin,
#     Seo, SeoAdmin,
# )
# admin.site.unregister(SiteConfig)
# admin.site.unregister(NotificationConfig)
# admin.site.unregister(CatalogueConfig)
# admin.site.unregister(DesignConfig)
# # admin.site.unregister(Translation)
# admin.site.unregister(Robots)
# admin.site.unregister(Seo)


# from box.seo.admin import (
#     ItemSeo, ItemSeoAdmin,
# )
# admin.site.unregister(ItemSeo)


# from box.imp_exp.admin import (
#     ImportLog, ImportLogAdmin
# )
# admin.site.unregister(ImportLog)





# ####################################################
# # unregister zone 

# try:
#     admin.site.unregister(Redirect)
#     admin.site.unregister(Site)
#     admin.site.unregister(Group)
# except:
#     pass

# try:
#     from django_celery_beat.models import *
#     admin.site.unregister(IntervalSchedule)
#     admin.site.unregister(CrontabSchedule)
#     admin.site.unregister(SolarSchedule)
#     admin.site.unregister(ClockedSchedule)
#     admin.site.unregister(PeriodicTask)
# except: 
#     pass 
# try:
#     from filebrowser.models import * 
#     admin.site.unregister(FileBrowser)
# except: 
#     pass
# try:
#     from allauth.account.models import * 
#     # admin.site.unregister(EmailConfirmation)
#     admin.site.unregister(EmailAddress)
# except: 
#     pass 
# try:
#     from django.contrib.flatpages.models import *
#     admin.site.unregister(FlatPage)
# except: 
#     pass 
# try:
#     from allauth.socialaccount.models import * 
#     admin.site.unregister(SocialApp)
#     admin.site.unregister(SocialToken)
#     admin.site.unregister(SocialAccount)
# except: 
#     pass








# ####################################################
# # admin plus zone 



# class AdminPlus(admin.AdminSite):
#     site_header = "Site Admin"
#     site_title  = "Site Admin"
#     index_title = "Site Admin"


# admin_plus = AdminPlus(name='admin_plus')
# try:
#     admin_plus.unregister(Redirect)
#     admin_plus.unregister(Site)
#     admin_plus.unregister(User)
#     admin_plus.unregister(Group)
#     admin_plus.unregister(Cart)
#     admin_plus.unregister(CartItem)
# except:
#     pass
