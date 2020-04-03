from .item_related import * 
from .item import * 
from .item_category import * 
from .attribute import * 
from . import * 



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



