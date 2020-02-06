from box.shop.item.models import ItemCategory, Item
from django.conf import settings 

def categories(request):
    categories = ItemCategory.objects.all().filter(parent=None)
    # for category in categories[0:1]:
    #     print()
    #     print()
    #     print('category:',  category)
    #     for subcategory in category.subcategories.all():#.filter(parent=category):
    #         print('subcategory:', subcategory)
    #         print('subcategory.parent:', subcategory.parent)
    MULTIPLE_CATEGORY = settings.MULTIPLE_CATEGORY
    
    return locals()


