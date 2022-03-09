from django import template

register = template.Library()


@register.filter
def dict_get(mapping, key):
    return mapping.get(key)
