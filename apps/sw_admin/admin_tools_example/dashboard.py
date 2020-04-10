from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.dashboard.modules import (
    DashboardModule, Group, LinkList, AppList, ModelList, RecentActions, Feed
)
from admin_tools.utils import get_admin_site_name

import admin_tools 


class HistoryDashboardModule(modules.LinkList):
    title = 'History'

    def init_with_context(self, context):
        request = context['request']
        history = request.session.get('history', [])
        for item in history:
            self.children.append(item)
        history.insert(0, {
            'title': context['title'],
            'url': request.META['PATH_INFO']
        })
        if len(history) > 10:
            history = history[:10]
        request.session['history'] = history


class MyModule(modules.DashboardModule):
    def is_empty(self):
        return self.message == ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template = 'my_block/hello.html'
        self.message = kwargs.get('message', '')
        self.babesage = kwargs.get('babesage', '')


class CustomIndexDashboard(Dashboard):
    def get_children(self, context):
        site_name = get_admin_site_name(context)
        children = [
            modules.LinkList(
                _('Quick links'),
                layout='inline',
                draggable=False,
                deletable=False,
                collapsible=False,
                children=[
                    [_('Return to site'), '/'],
                    [_('Change password'),
                    reverse('%s:password_change' % site_name)],
                    [_('Log out'), reverse('%s:logout' % site_name)],
                ]
            ),
            modules.AppList(
                title=_('Applications'),
                exclude=('django.contrib.*',),
            ),
            modules.AppList(
                title=_('Administration'),
                models=('django.contrib.*',),
            ),
            modules.Feed(
                # _('Latest Django News'),
                _('Latest Reddit News'),
                # feed_url='http://www.djangoproject.com/rss/weblog/',
                feed_url='https://www.reddit.com/r/worldnews/.rss',
                limit=5
            ),
            modules.LinkList(
                _('Support'),
                children=[
                    {
                        'title': _('Django documentation'),
                        'url': 'http://docs.djangoproject.com/',
                        'external': True,
                    },
                    {
                        'title': _('Django "django-users" mailing list'),
                        'url': 'http://groups.google.com/group/django-users',
                        'external': True,
                    },
                    {
                        'title': _('Django irc channel'),
                        'url': 'irc://irc.freenode.net/django',
                        'external': True,
                    },
                ]
            ),
            modules.ModelList(
                title = u'Пользователи',
                models=(
                    'django.contrib.auth.*',
                    'my_accounts.models.Profile',
                ),
            ),
            modules.Group(
                title=u"Статистика",
                display="tabs",
                children=[
                    MyModule(),
                    # nadovmeste_modules.Overview(),
                    # nadovmeste_modules.Subscribers(),
                    # nadovmeste_modules.Finances(),
                    # nadovmeste_modules.Users(),
                ]
            ),
            MyModule(
                title=u"Приветствие", 
                message = u'Привет!',
                babesage = 'goodbye',
            ),
            modules.RecentActions(
                title=_('Recent Actions'),
                limit=5
            ),
            # HistoryDashboardModule(),
            HistoryDashboardModule(
                enabled=True, 
                draggable=True, 
                collapsible=True, 
                deletable=True,
                title='Історія',
                title_url=None,
                css_classes=None,
                pre_content=None,
                post_content=None,
                content=None,
                # template="admin_tools/dashboard/module.html"
            ),
            modules.Group(
                title="My Group",
                display="tabs",
                # display="accordion",
                # display="stacked",
                children=[
                    modules.AppList(
                        title="Shop",
                        models=['box.apps.sw_shop.sw_catalog.models.Item',]
                    ),
                    modules.AppList(
                        title="Apps",
                        exclude=['box.*',]
                    ),
                    
                ]
            ),
            modules.LinkList(
                # layout='inline',
                layout='stacked',
                children=(
                    {
                        'title': 'Python website',
                        'url': 'http://www.python.org',
                        'external': True,
                        'description': 'Python language rocks !',
                        'attrs': {'target': '_blank'},
                    },
                    ['Django', 'http://www.djangoproject.com', True],
                    ['Some internal link', '/some/internal/link/'],
                )
            ),
            modules.AppList(
                title='Administration',
                models=('django.contrib.*',)
            ),
            modules.AppList(
                title='Applications',
                exclude=('django.contrib.*',)
            ),
            modules.ModelList(
                title='Authentication',
                models=['django.contrib.auth.*',]
            ),
            modules.RecentActions(
                title='Django CMS recent actions',
                include_list=('box.page', 'box.apps.sw_admin',)
            ),
        ]
        return children
    

    # class Media:
    #     css = {
    #         'screen, projection': ('css/mydashboard.css',),
    #     }
    #     js = ('js/mydashboard.js',)

    title = 'Admin'
    # template = 'sw_admin/index.html'
    # template = 'admin/index.html'

    # def __init__(self, **kwargs):
    #     Dashboard.__init__(self, **kwargs)
    #     self.children = self.get_children()

    # columns = 1
    def get_columns(self, context):
        request = context['request']
        if not request.session.get('columns'):
            request.session['columns'] = 2
        columns = request.session.get('columns')
        return columns

    def init_with_context(self, context):
        self.children = self.get_children(context)
        self.columns  = self.get_columns(context)
        context.update({
            'babaski':'mapazgi',
        })
        return super().init_with_context(context)


class CustomAppIndexDashboard(AppIndexDashboard):
    def get_children(self, *args, **kwargs):
        children = [
            modules.ModelList(
                self.app_title, 
                self.models
            ),
            modules.RecentActions(
                title=_('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            ),
            # modules.RecentActions(
            #     include_list=self.models,
            #     limit=5
            # ),

        ]
        return children 

    title = 'sdf'

    # def __init__(self, *args, **kwargs):
    #     AppIndexDashboard.__init__(self, *args, **kwargs)
    #     self.children = self.get_children(*args, **kwargs)

    def init_with_context(self, context):
        self.children = self.get_children()
        context.update({
            'sdf':'sdf',
        })
        return super().init_with_context(context)


