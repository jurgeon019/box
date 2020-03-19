from box.seo.models import *
from box.design.models import *
from box.global_config.models import *


def context(request):
    seo    = Seo.get_solo()
    config = SiteConfig.get_solo()
    design = DesignConfig.get_solo()
    catalogue = CatalogueConfig.get_solo()
    print(design.favicon_type)
    return locals()
