from box.global_config.models import SiteConfig
from box.seo.models import Robots, Seo
from box.design.models import DesignConfig


def context(request):
    seo    = Seo.get_solo()
    config = SiteConfig.get_solo()
    design = DesignConfig.get_solo()
    return locals()
