# -*- coding: utf-8 -*-
import json
import urllib2
import logging
from os import path
from random import random
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from settings import *

logger = logging.getLogger(__package__)


@receiver(post_save, sender=get_user_model())
def rc_create_user(sender, **kwargz):
    user = kwargz.get('instance')
    new = kwargz.get('created')

    if not new:
        return

    url = path.join(API, 'users.create')
    data = json.dumps({
        'name'    : user.get_full_name() or user.username,
        'email'   : user.email,
        'password': '%d%f' % (user.id, random()),
        'username': user.username,
        'verified': True,
    })

    headers = {'Content-Length': len(data)}
    headers.update(HEADERS)

    request  = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.HTTPError as e:
        logger.error(e)
