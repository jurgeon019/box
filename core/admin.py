from django.contrib import admin
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site

from box.payment.liqpay.admin import (
    Payment, PaymentAdmin,
)


####################################################
# unregister zone 

try:
    admin.site.unregister(Redirect)
    admin.site.unregister(Site)
    admin.site.unregister(Group)
except:
    pass


try:
    from django_celery_beat.models import *
    admin.site.unregister(IntervalSchedule)
    admin.site.unregister(CrontabSchedule)
    admin.site.unregister(SolarSchedule)
    admin.site.unregister(ClockedSchedule)
    admin.site.unregister(PeriodicTask)
except: 
    pass 
try:
    from filebrowser.models import * 
    admin.site.unregister(FileBrowser)
except: 
    pass
try:
    from allauth.account.models import * 
    # admin.site.unregister(EmailConfirmation)
    admin.site.unregister(EmailAddress)
except: 
    pass 
try:
    from django.contrib.flatpages.models import *
    admin.site.unregister(FlatPage)
except: 
    pass 
try:
    from allauth.socialaccount.models import * 
    admin.site.unregister(SocialApp)
    admin.site.unregister(SocialToken)
    admin.site.unregister(SocialAccount)
except: 
    pass


