from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings 

from admin_tools.dashboard import (
    modules,
    Dashboard, AppIndexDashboard, 
    DefaultIndexDashboard, 
    DefaultAppIndexDashboard,
)
from admin_tools.dashboard.modules import (
    DashboardModule, Group, LinkList, AppList, ModelList, RecentActions, Feed
)

from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(DefaultIndexDashboard):
    columns = 3

    # def get_columns(self, context):
    #     request = context['request']
    #     if not request.session.get('columns'):
    #         request.session['columns'] = 4
    #     columns = request.session.get('columns')
    #     return columns

    def init_with_context(self, context):
        # self.columns  = self.get_columns(context)
        site_name = get_admin_site_name(context)
        if "box.apps.sw_shop" in settings.INSTALLED_APPS:
            self.children.append(modules.AppList(
                _('Магазин'),
                models=('box.apps.sw_shop.*',),
            ))
        if "box.apps.sw_dev" in settings.INSTALLED_APPS:
            self.children.append(modules.AppList(
                _('Розробка'),
                models=('box.apps.sw_dev.*',),
            ))
        if "box.apps.sw_blog" in settings.INSTALLED_APPS:
            self.children.append(modules.AppList(
                _('Блог'),
                models=('box.apps.sw_blog.*',),
            ))
        if "box.apps.sw_payment" in settings.INSTALLED_APPS:
            self.children.append(modules.AppList(
                _("Оплати"),
                models=('box.apps.sw_payment.*',),
            ))
        if 'box.apps.sw_delivery' in settings.INSTALLED_APPS:
            self.children.append(modules.AppList(
                _("Доставки"),
                models=('box.apps.sw_delivery.*',),
            ))

        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=True,
            deletable=True,
            collapsible=True,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.AppList(
            _('Applications'),
            exclude=(
                'django.contrib.*',
                'box.*',
            ),
        ))

        # TODO: циклом зробити так шоб кожну аппку з box.core.* в адмінці можна було перетягувати
        # і приховувати. Підсказка: django.apps.apps.get_model + django.conf.INTSALLED_APPS

        self.children.append(modules.AppList(
            _("Налаштування"),
            models=('box.core.*',),
            exclude=(
                'box.core.sw_contact_form.*',
                'box.core.sw_content.*',
            ),
        ))
        
        self.children.append(modules.AppList(
            _("Зворотній звязок"),
            models=('box.core.sw_contact_form.*',),
        ))


        self.children.append(modules.AppList(
            _("Контент"),
            models=('box.core.sw_content.*',),
        ))


        # self.children.append(modules.AppList(
        #     _("Global"),
        #     models=('box.*'),
        #     exclude=(
        #         'django.contrib.*',
        #         'box.core.*',
        #         'box.apps.sw_shop.*',
        #         'box.apps.sw_blog.*',
        #         'box.apps.sw_payment.*',
        #     )
        # )),



        # self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append a feed module
        # self.children.append(modules.Feed(
        #     _('Latest Django News'),
        #     feed_url='http://www.djangoproject.com/rss/weblog/',
        #     limit=5
        # ))

        # self.children.append(modules.LinkList(
        #     _('Support'),
        #     children=[
        #         {
        #             'title': _("Сайт розробників"),
        #             "url": "https://starwayua.com",
        #             'external': True,
        #         },
        #         {
        #             'title': _('Django documentation'),
        #             'url': 'http://docs.djangoproject.com/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Django "django-users" mailing list'),
        #             'url': 'http://groups.google.com/group/django-users',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Django irc channel'),
        #             'url': 'irc://irc.freenode.net/django',
        #             'external': True,
        #         },
        #     ]
        # ))


class CustomAppIndexDashboard(DefaultAppIndexDashboard):
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]



