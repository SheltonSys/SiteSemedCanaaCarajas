# em templatetags/extras.py
from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key, '')
    return ''


@register.filter
def dict(d, key):
    return d.get(key, '')