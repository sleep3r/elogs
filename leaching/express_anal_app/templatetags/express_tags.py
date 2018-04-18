from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag()
def model_desc(obj):
    if obj.__doc__:
        return mark_safe('<p>{}</p>'.format(obj.__doc__))
    return ''

@register.filter(name='formcontrol')
def addclass(value):
    return value.as_widget(attrs={'class': 'form-control'})

@register.filter(name='formatDate')
def addclass(value):
    return value