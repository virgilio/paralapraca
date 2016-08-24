from django import template

register = template.Library()


@register.filter
def units_ratio(units_list):
    if len(units_list) > 20:
        return 1
    return 7 - len(units_list) / 3
