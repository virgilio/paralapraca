# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    url(r'^o2/me/?', views.OAuth2UserInfoView.as_view(), name='oauth2_provider_userinfo'),
]
