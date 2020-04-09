from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import (
    items, Menu, DefaultMenu
)
from admin_tools.menu.items import MenuItem, AppList, ModelList, Bookmarks



class CustomMenu(DefaultMenu):
    pass 

