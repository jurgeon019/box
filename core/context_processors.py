from box.global_config.models import *
from box.core import settings as core_settings 

def context(request):
    seo        = Seo.get_solo()
    config     = SiteConfig.get_solo()
    design     = DesignConfig.get_solo()
    catalogue  = CatalogueConfig.get_solo()
    show_admin = core_settings.SHOW_ADMIN 
    return locals()
