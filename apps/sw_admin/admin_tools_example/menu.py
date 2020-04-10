from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu
from admin_tools.menu.items import MenuItem, AppList, ModelList, Bookmarks


class HistoryMenuItem(items.MenuItem):
    title = 'History'

    def init_with_context(self, context):
        request = context['request']
        history = request.session.get('history', [])
        for item in history:
            self.children.append(items.MenuItem(
                title=item['title'],
                url=item['url'],
            ))
        view = {
            'title': context['title'],
            'url': request.META['PATH_INFO']
        }
        # try:
        #     history.insert(0, view)
        #     if len(history) > 10:
        #         history = history[:10]
        #     request.session['history'] = history
        # except:
        #     print('Відвалюється при переході на зміну паролю')


class CustomMenu(Menu):
    # class Media:
    #     css = {
    #         'all': (
    #             # 'css/mymenu.css',
    #             # '',
    #         )
    #     }
    #     js = (
    #         # 'js/mymenu.js',
    #     )
    template = "admin_tools/menu/menu.html"
    # template = "sw_admin/menu/menu.html"
    def get_children(self):
        children = [
            items.AppList(
                title=_('Applications'),
            ),
            # items.AppList(
            #     title=_('Applications'),
            #     exclude=('django.contrib.*',),
            #     exclude_list=('django.contrib.*'),
            # ),
            # items.AppList(
            #     title=_('Administration'),
            #     models=('django.contrib.*',)
            # ),

            items.MenuItem(
                title=_('Dashboard'), 
                url=reverse('admin:index')
            ),
            items.MenuItem(
                title='Multi level menu item',
                children=[
                    items.MenuItem(title='Child 1', url='/foo/'),
                    items.MenuItem(title='Child 2', url='/bar/'),
                ]
            ),
            HistoryMenuItem(),
            items.Bookmarks(),
            # items.Bookmarks(
            #     'My bookmarks'
            # ),
            items.ModelList(
                'Authentication', 
                # ['django.contrib.auth.*',]
                ['box.apps.sw_shop.sw_catalog.*',],
            )
        ]
        return children


    # def __init__(self, **kwargs):
    #     # Menu.__init__(self, **kwargs)
    #     super().__init__(**kwargs)
    #     # self.template = "admin_tools/menu/menu.html"
    #     self.children += self.get_children()

    def init_with_context(self, context):
        context.update({
            'babaski':'HELLO BLYA',
        })
        self.children += self.get_children()
        return super().init_with_context(context)



