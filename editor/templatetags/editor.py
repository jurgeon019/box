from django import template
from django.shortcuts import render 

from ..main import render_content

register = template.Library()


@register.inclusion_tag('editor/plain.html')
def plain(code, page_code=None):
    result = render_content(code=code, content_type='plain', page_code=page_code)
    return result 


@register.inclusion_tag('editor/tiny.html')
def tiny(code, page_code=None):
    result = render_content(code=code, content_type='tiny', page_code=page_code)
    return result 


@register.inclusion_tag('editor/image.html')
def render_image(code, page_code=None):
    result = render_content(code=code, content_type='image', page_code=page_code)
    return result 

from django.template.loader import render_to_string 


@register.inclusion_tag('editor/slider.html')
def render_slider(code, page_code=None):
    result = render_content(code=code, content_type='slider', page_code=page_code)
    return result



@register.tag
def placeholder1(parser, token):
    nodelist = parser.parse(('endplaceholder1',))
    parser.delete_first_token()
    return Placeholder1Node(nodelist)

class Placeholder1Node(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist 
    
    def render(self, context):
        output = self.nodelist.render(context)
        output = \
            '< div class="modal fade" id="myModal" tabindex="-1" role="dialog" ' \
            '    aria-labelledby="myModalTitle" aria-hidden="true">' \
            '    < div class="modal-dialog modal-dialog-centered" role="document">' \
            '        < div class="modal-content">' \
            '            < div class="modal-header">' \
            '                < h5 class="modal-title" id="myModalTitle">Modal title</h5>' \
            '                < button type="button" class="close" data-dismiss="modal" aria-label="Close">' \
            '                    < span aria-hidden="true">×</span>' \
            '                </button>' \
            '             </div>' \
            '             < div class="modal-body">' \
            f'                {self.nodelist.render(context)}' \
            '            </div>' \
            '        </div>' \
            '    </div>' \
            '</div>'
        return output




@register.tag
def placeholder2(parser, token):
    contents = token.split_contents()
    print(contents)
    try:
        tag_name, modal_id, title = contents
    except:
        pass 

    nodelist = parser.parse(('endplaceholder2',))
    parser.delete_first_token()
    return Placeholder2Node(nodelist)

class Placeholder2Node(template.Node):
    def __init__(self, modal_id, title, nodelist):
        self.modal_id = modal_id
        self.title = title 
        self.nodelist = nodelist 
    
    def render(self, context):
        output = self.nodelist.render(context)
        return output











###################



@register.simple_tag
def get_feature(page_code, page_text_code):
    page    = Page.objects.get(code=page_code)
    print(page)
    feature = page.features.get(code=page_text_code)
    return feature


@register.simple_tag
def get_features_by_attr(page_code, attr):
    page    = Page.objects.get(code=page_code)
    # sliders = page.sliders.all()
    sliders = getattr(page, attr).all()
    return sliders


@register.simple_tag
def get_features_by_class(page_code, classname):
    import sys 
    page    = Page.objects.get(code=page_code)
    # sliders = Slider.objects.filter(page__code=page_code)
    sliders = getattr(sys.modules[__name__], classname).objects.filter(page__code=page_code)
    return sliders




'''
{% load get_feature get_features_by_attr from get %}

{% block content %}

{% get_feature "index" "char1" as content1 %} 
{% get_features_by_attr "index" "sliders" as sliders %}
{% get_features_by_attr "index" "features" as features %}
{{content1.name}}
<br>
{{content1.value}}
<br>
{{sliders}}
<br>
{% for feature in features%}
{{feature.name}}
<br>
{{feature.value}}
{% endfor%}

{%endblock content%}


'''