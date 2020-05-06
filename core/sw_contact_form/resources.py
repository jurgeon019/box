from import_export.resources import ModelResource 

from .models import * 


class ContactRecipientEmailResource(ModelResource):
    class Meta:
        model = ContactRecipientEmail
        exclude = []



class ContactConfigResource(ModelResource):
    class Meta:
        model = ContactConfig
        exclude = []



