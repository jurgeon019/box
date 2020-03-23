from import_export.resources import ModelResource
from .models import *
from box.core.utils import get_multilingual_fields 



class AbstractContentResource(ModelResource):
    def get_export_order(self):
        export_order = [
            # '',
        ]
        return export_order
    def get_import_id_fields(self):
        import_id_fields = [

        ]
        return import_id_fields



class AbstractTextResource(ModelResource):
    def get_export_order(self):
        export_order = [
            # '',
        ]
        return export_order
    def get_import_id_fields(self):
        import_id_fields = [

        ]
        return import_id_fields



class AbstractLinkResource(ModelResource):
    def get_export_order(self):
        export_order = [
            # '',
        ]
        return export_order
    def get_import_id_fields(self):
        import_id_fields = [

        ]
        return import_id_fields




class MapResource():
    class Meta:
        model = Map 
        exclude = [

        ]


class ImgResource():
    class Meta:
        model = Img 
        exclude = [

        ]


class TextResource():
    class Meta:
        model = Text 
        exclude = [

        ]


class AddressResource():
    class Meta:
        model = Address 
        exclude = [

        ]


class TelResource():
    class Meta:
        model = Tel 
        exclude = [

        ]


class MailtoResource():
    class Meta:
        model = Mailto 
        exclude = [

        ]


class LinkResource():
    class Meta:
        model = Link 
        exclude = [

        ]


# Social




class TextResource(ModelResource):
    
    class Meta:
        model = Text 
        exclude = [
            'id',
            'created',
            'updated',
        ]

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            'page',
            'code',
            *multilingual_fields['text']
        ]
        return export_order

    def get_import_id_fields(self):
        import_id_fields = [
            'code',
        ]
        return import_id_fields

    def dehydrate_page(self, obj):
        page = None 
        if obj.page:
            page = obj.page.code 
        return page 

    def before_import_row(self, row, **kwargs):
        if row['page']:
            row['page'] = Page.objects.get_or_create(code=row['page'])[0].id


class ImgResource(ModelResource):
    # TODO: не імпортується alt_ru

    class Meta:
        model = Img 
        exclude = [
            'id',
            'created',
            'updated',
        ]

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            'page',
            'code',
            'image',
            *multilingual_fields['alt'],
        ]
        return export_order

    def get_import_id_fields(self):
        import_id_fields = [
            'code',
        ]
        return import_id_fields

    def dehydrate_page(self, feature):
        page = None 
        if feature.page:
            page = feature.page.code 
        return page 
    
    def before_import_row(self, row, **kwargs):
        # print('row:', row)
        if row['page']:
            row['page'] = Page.objects.get_or_create(code=row['page'])[0].id



class PageResource(ModelResource):
    class Meta:
        model = Page
        exclude = [
            'id',
            'created',
            'updated',
        ]

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            'code',
            *multilingual_fields['meta_title'],
            *multilingual_fields['meta_descr'],
            *multilingual_fields['meta_key'],
        ]
        return export_order

    def get_import_id_fields(self):
        import_id_fields = [
            'code',
        ]
        return import_id_fields







from import_export.resources import ModelResource 

from .models import * 
from box.page.models import Page 
from box.core.utils import get_multilingual_fields



class SlideResource(ModelResource):
    class Meta:
        model = Slide 
        exclude = [
            'id',
            'created',
            'updated',
            # 'order',
            'page',
        ]
       

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        export_order = [
            'code',
            # 'page',
            'slider',
            'image',
            *multilingual_fields['alt'],
            *multilingual_fields['title'],
        ]
        return export_order 

    def get_import_id_fields(self):
        fields = [
            'code',
        ]
        return fields 

    # def dehydrate_page(self, obj):
    #     page = None 
    #     if obj.page:
    #         page = obj.page.code 
    #     return page 
    
    def dehydrate_slider(self, obj):
        slider = None 
        if obj.slider:
            slider = obj.slider.code 
        return slider 

    def before_import_row(self, row, **kwargs):
        # if row['page']:
        #     row['page'] = Page.objects.get_or_create(code=row['page'])[0].id
        if row['slider']:
            row['slider'] = Slider.objects.get_or_create(code=row['slider'])[0].id


class SliderResource(ModelResource):
    class Meta:
        model = Slider
        exclude = [
            'id',
            'created',
            'updated',
            'order',
        ]

    def get_export_order(self):
        multilingual_fields = get_multilingual_fields(self._meta.model)
        order = [
            'code',
            'page',
            'name',
        ]
        return order 
    
    def get_import_id_fields(self):
        fields = [
            'code',
        ]
        return fields 

    def dehydrate_page(self, obj):
        page = None 
        if obj.page:
            page = obj.page.code 
        return page 

    def before_import_row(self, row, **kwargs):
        if row['page']:
            row['page'] = Page.objects.get_or_create(code=row['page'])[0].id



