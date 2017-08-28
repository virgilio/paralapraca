# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'answer-notification', views.AnswerNotificationViewSet)
router.register(r'unread-notification', views.UnreadNotificationViewSet)
router.register(r'contract', views.ContractViewSet)
router.register(r'summary', views.SummaryViewSet, base_name='summary')
router.register(r'users-by-group', views.UsersByGroupViewSet, base_name='users-by-group')
router.register(r'users-by-class', views.UsersByClassViewSet, base_name='users-by-class')

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    url(r'^api/', include(router.urls)),
    url(r'^chat/?$', views.ChatScreenView.as_view(template_name="chat.html"), name='chat_screen'),
    url(r'^_chat/auth/$', views.RocketchatIframeAuthView.as_view(), name='rocketchat_iframe_auth'),
    url(r'^profile/edit/?$', views.ProfileEditView.as_view(), name="profile_edit"),
]
