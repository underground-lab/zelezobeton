from django import template

register = template.Library()


@register.filter
def dict_get(mapping, key):
    return mapping.get(key)


@register.filter
def values_attr(mapping, attr_name):
    """Map attribute getter on dictionary values."""
    return [getattr(value, attr_name) for value in mapping.values()]


@register.filter
def listing_czech(strings):
    if not strings:
        return
    *leading, last = strings
    if not leading:
        return last
    leading = ', '.join(leading)
    return f'{leading} a {last}'


@register.filter
def sort_by_index(iterable, sort_order):
    return sorted(iterable, key=sort_order.index)
