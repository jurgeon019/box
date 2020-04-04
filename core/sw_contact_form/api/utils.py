from ..models import *

fields = [field.name for field in Contact._meta.fields]
contact_get = {
    'method':'POST',
    'fields':[
        {
            'fieldname':'name',
            'type':'CharField',
            'max_length':'255',
        },
        {
            'fieldname':'email',
            'type':'EmailField',
            'max_length':'255',
        },
        {
            'fieldname':'phone',
            'type':'CharField',
            'max_length':'255',
        },
        {
            'fieldname':'message',
            'type':'TextField',
        },
        {
            'sdf':fields,
        }
    ]
}

