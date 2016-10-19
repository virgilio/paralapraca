# -*- coding: utf-8 -*-
import json
from oauth2_provider.views import ProtectedResourceView
from oauth2_provider.models import AccessToken
from django.http import HttpResponse, HttpResponseForbidden

class OAuth2UserInfoView(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('access_token', '')
        access_token = AccessToken.objects.filter(token=token).first()

        if access_token:
            user = access_token.user
            return HttpResponse(json.dumps({
                'id': user.id,
                'email': user.email
            }));

        return HttpResponseForbidden('Ivalid or empty token')
