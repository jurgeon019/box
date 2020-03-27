from django.contrib import admin
from project.models import * 


class ContactFormAdmin(admin.ModelAdmin):
    pass 


admin.site.register(ContactForm, ContactFormAdmin)



