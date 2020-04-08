from django import template
from django.shortcuts import render 
from django.template.loader import render_to_string 

from ..editor import get_context


register = template.Library()


@register.simple_tag
def placeholder(content_type, code, page_code=None):
    '''
    {% placeholder 'image' 'img1_jpg'  %}
    '''
    context = get_context(content_type=content_type, code=code, page_code=page_code)
    return render_to_string(f'content/{content_type}.html', context=context)


@register.simple_tag
def render(content_type, code, page_code=None):
    '''
    {% render 'image' 'img_jpg_1' as img_jpg_1 %}

    {{img_jpg_1.text}}
    
    {{img_jpg_1.href}}

    {{img_jpg_1.html|safe}}
    '''
    context = get_context(content_type=content_type, code=code, page_code=page_code)
    return context['obj']



































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



# @register.simple_tag
# def get_feature(page_code, page_text_code):
#     page    = Page.objects.get(code=page_code)
#     print(page)
#     feature = page.features.get(code=page_text_code)
#     return feature


# @register.simple_tag
# def get_features_by_attr(page_code, attr):
#     page    = Page.objects.get(code=page_code)
#     # sliders = page.sliders.all()
#     sliders = getattr(page, attr).all()
#     return sliders


# @register.simple_tag
# def get_features_by_class(page_code, classname):
#     import sys 
#     page    = Page.objects.get(code=page_code)
#     # sliders = Slider.objects.filter(page__code=page_code)
#     sliders = getattr(sys.modules[__name__], classname).objects.filter(page__code=page_code)
#     return sliders




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