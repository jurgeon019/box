from box.apps.sw_shop.sw_catalog.models import ItemCategory


def context(request):
    # parts_category     = ItemCategory.objects.get(code="parts")
    try:
        parts_category     = ItemCategory.objects.get(code="parts")
    except:
        pass
    try:
        spec_rent_category = ItemCategory.objects.get(code="spec_rent")
    except:
        pass
    try:
        spec_sell_category = ItemCategory.objects.get(code="spec_sell")
    except:
        pass
    try:
        jcb_category = ItemCategory.objects.get(code='jcb_parts')
    except:
        pass
    return locals()




