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


@register.simple_tag()
def fid(field_id, index=None):
    return '{% include "value.html" with fid=' + str(field_id) + ' index=' + str(index) + ' %}'


@register.filter
def keyval(dict, key):
    return dict[key]


@register.inclusion_tag('value.html', takes_context=True)
def choose_val(field_info, index):
    if index:
        return {'val': field_info[index]}
    else:
        return {'val': field_info}