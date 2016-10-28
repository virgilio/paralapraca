# -*- coding: utf-8 -*-
from os import path
from django.conf import settings

ROCKET_CHAT = {
    'address'   : 'http://chat.paralapraca.org.br',
    'service'   : 'paralapraca',
    'auth_token': '',
    'user_id'   : '',
}

ROCKET_CHAT.update(getattr(settings, 'ROCKET_CHAT', {}))

API     = path.join(ROCKET_CHAT['address'], 'api/v1')

HEADERS = {
    'X-Auth-Token': ROCKET_CHAT['auth_token'],
    'X-User-Id'   : ROCKET_CHAT['user_id'],
    'Content-type':'application/json',
}

__all__ = (
    'API',
    'HEADERS',
    'ROCKET_CHAT',
)