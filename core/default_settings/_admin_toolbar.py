# ADMIN_TOOLS_INDEX_DASHBOARD = 'box.apps.sw_admin.dashboard.CustomIndexDashboard'
# or
ADMIN_TOOLS_INDEX_DASHBOARD = {
    # 'django.contrib.admin.site': 'admin_tools.dashboard.dashboards.DefaultIndexDashboard',
    'django.contrib.admin.site': 'box.apps.sw_admin.dashboard.CustomIndexDashboard',
    # 'project.admin.admin_site': 'project.dashboard.CustomIndexDashboard',
    # 'other_app.admin.admin_site': 'other_app.dashboard.CustomIndexDashboard',
}
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'box.apps.sw_admin.dashboard.CustomAppIndexDashboard'
# or
ADMIN_TOOLS_APP_INDEX_DASHBOARD = {
    # 'django.contrib.admin.site': 'admin_tools.dashboard.dashboards.DefaultAppIndexDashboard',
    'django.contrib.admin.site': 'box.apps.sw_admin.dashboard.CustomAppIndexDashboard',
    # 'project.admin.admin_site': 'project.dashboard.CustomAppIndexDashboard',
    # 'other_app.admin.admin_site': 'other_app.dashboard.CustomAppIndexDashboard',
}
# ADMIN_TOOLS_MENU = 'box.apps.sw_admin.menu.CustomMenu'
# or
ADMIN_TOOLS_MENU = {
    # 'django.contrib.admin.site': 'admin_tools.menu.DefaultMenu',
    'django.contrib.admin.site': 'box.apps.sw_admin.menu.CustomMenu',
    # 'project.admin.admin_site': 'project.menu.CustomMenu',
    # 'other_app.admin.admin_site': 'other_app.menu.CustomMenu',
}


# Обнуляет логотип "Джанго"
ADMIN_TOOLS_THEMING_CSS = 'sw_admin/css/theming.css' 
# ADMIN_TOOLS_THEMING_CSS = 'admin_tools/media/admin_tools/css/theming.css' 






