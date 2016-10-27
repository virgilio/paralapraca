# -*- coding: utf-8 -*-
import json
import urllib2
from os import path
from random import random

from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


ROCKET_CHAT = getattr(settings, 'ROCKET_CHAT', {
    'address'   : 'http://chat.paralapraca.org.br',
    'service'   : 'paralapraca',
    'auth_token': '',
    'user_id'   : '',
})

API     = path.join(ROCKET_CHAT['address'], 'api/v1')
HEADERS = {
    'X-Auth-Token': ROCKET_CHAT['auth_token'],
    'X-User-Id'   : ROCKET_CHAT['user_id'],
    'Content-type':'application/json',
}

@receiver(user_logged_out, sender=get_user_model())
def rc_logout_user(sender, user, request, **kwargz):
    print 'test', sender, user


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
    response = urllib2.urlopen(request)
    return response.read()
