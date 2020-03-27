from django.contrib import admin
from dev.models import * 


class ContactFormAdmin(admin.ModelAdmin):
    pass 


admin.site.register(ContactForm, ContactFormAdmin)



