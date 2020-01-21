from django.urls import path 
from .views import * 

static_urls = [
    path('',                     index,    name='starway_index'),
    path('contacts/',            contacts, name='starway_contacts'),
    path('profile/',             profile,  name='starway_profile'),
    path('service_categories/',  service_categories, name='starway_service_categories'),
    path('case_categories/',     case_categories,    name='starway_case_categories'),
    path('about/',               about,         name='starway_about'),
    path('how_it_works/',        how_it_works,  name='starway_how_it_works'),
    path('story/',               story,         name='starway_story'),
    path('team/',                team,          name='starway_team'),
    path('become_member/',       become_member, name='starway_become_member'),
]

dynamic_urls = [
    path('services_list/<slug>/', services_list, name='starway_services_list'),
    path('service/<slug>/',       service,       name='starway_service'),
    path('cases_list/<slug>/',    cases_list,    name='starway_cases_list'),
    path('case/<slug>/',          case,          name='starway_case'),
    path('member/<slug>',         member,        name='starway_member'),
]

urlpatterns = []
urlpatterns += static_urls
urlpatterns += dynamic_urls