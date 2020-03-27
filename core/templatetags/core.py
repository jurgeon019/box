from typing import Optional, Any, Dict

from django import urls, template

from box.global_config.models import SiteConfig
from box.seo.models import Robots, SeoScript


register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context: Dict[str, Any], language: Optional[str]) -> str:
    """
        {% translate_url 'en' %}
    """
    url = context['request'].build_absolute_uri()
    return urls.translate_url(url, language)



@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def query(qs, **kwargs):
    """ 
        {% query books author=author as mybooks %}
        {% for book in mybooks %}
          {{book}}
        {% endfor %}
    """
    return qs.filter(**kwargs)


@register.filter
def in_category(things, category):
    '''
        {% for category in categories %}
            {% for thing in things|in_category:category %}
                {{ thing }}
            {% endfor %}
        {% endfor %}
    '''
    return things.filter(category=category)


@register.filter
def in_slider(slides, slider):
    '''
        {% for slide in slides|in_slider:slider %}
            {{slide.image_url}}
        {% endfor %}
    '''
    return slides.filter(slider=slider)










# simple_tag

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag(takes_context=True)
def current_time(context, format_string):
    timezone = context['timezone']
    return your_get_current_time_method(timezone, format_string)



@register.simple_tag
def render_robots():
    robots = SiteConfig.get_solo().robots_txt
    return locals()



# inclusion_tag

@register.inclusion_tag('results.html')
def show_results(poll):
    choices = poll.choice_set.all()
    return {'choices': choices}

@register.inclusion_tag('link.html', takes_context=True)
def jump_link(context):
    return {
        'link': context['home_link'],
        'title': context['home_title'],
    }


@register.inclusion_tag('my_template.html')
def my_tag(a, b, *args, **kwargs):
    warning = kwargs['warning']
    profile = kwargs['profile']
    ...
    return ...


@register.inclusion_tag('core/renders/ogimages.html')
def render_ogimages():
    square    = SiteConfig.get_solo().og_image_square.url
    rectangle = SiteConfig.get_solo().og_image_rectangle.url
    return locals()


@register.inclusion_tag('core/renders/favicon.html')
def render_favicon():
    favicon = SiteConfig.get_solo().favicon.url
    return locals()









# filter

@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')

@register.filter(name='lower')
def lower(value): 
    return value.lower()

register.filter('lower', lower)
register.filter('cut', cut)



"""
{{ somevariable|cut:"0" }}
{{ somevariable|lower }}
"""