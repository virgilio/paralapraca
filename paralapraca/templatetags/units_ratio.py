from django import template

register = template.Library()


@register.filter
def units_ratio(units_list):
    if len(units_list) > 20:
        return 0.5
    return 7 - len(units_list) / 3
