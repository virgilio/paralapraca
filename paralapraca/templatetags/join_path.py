# -*- coding: utf-8 -*-
import os
from django import template

register = template.Library()

@register.simple_tag
def join_path(*args):
    return os.path.join(*args)
