from pprint import pprint

from django import template
from django.utils.html import mark_safe
from utils.deep_dict import deep_dict

register = template.Library()


class UnfilledCell():
    def __str__(self):
        return "Unfilled"


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
def value(fid, index=None):
    return '{% include "value.html" with field_name=' + str(fid) + ' index=' + str(index) + ' %}'


@register.filter
def keyval(dict, key):
    return dict[key]


@register.filter
def table_keyval(dict, key):
    return dict.get(key, deep_dict())


@register.filter
def cell_keyval(dict, key):
    return dict.get(key, UnfilledCell())


@register.filter
def choose_val(field_info, index):
    if index is not None:
        return field_info[index]
    else:
        return field_info


@register.filter
def choose_val_special(field_info, index):
    if index is None or isinstance(field_info, UnfilledCell):
        return field_info
    else:
        return field_info[index]


@register.filter
def stack(a, b):
    return a + b



@register.filter()
def to_num(value):
    return round(float(value), 2)


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)
