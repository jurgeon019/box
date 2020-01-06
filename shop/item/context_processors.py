from shop.item.models import ItemCategory, Item


def categories(request):
    categories = ItemCategory.objects.all().filter(parent=None)
    # for category in categories[0:1]:
    #     print()
    #     print()
    #     print('category:',  category)
    #     for subcategory in category.subcategories.all():#.filter(parent=category):
    #         print('subcategory:', subcategory)
    #         print('subcategory.parent:', subcategory.parent)
            
    return locals()


