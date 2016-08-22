from django import template

register = template.Library()


@register.filter
def units_ratio(units_list):
    return 7 - len(units_list) / 4
