

def get_admin_url(obj=None, action='change'):
    if obj:
        id = obj.id
        model_name = obj._meta.model_name 
        app_label = obj._meta.app_label 
        return f"/admin/{app_label}/{model_name}/{id}/{action}"
    return ''

