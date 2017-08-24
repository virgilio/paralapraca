# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from paralapraca.models import AnswerNotification, UnreadNotification
from paralapraca.serializers import AnswerNotificationSerializer, UnreadNotificationSerializer


ROCKET_CHAT = {
    'address': 'http://chat.paralapraca.org.br',
    'service': 'paralapraca'
}


class ChatScreenView(TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super(ChatScreenView, self).get_context_data(**kwargs)
        context['rocketchat'] = getattr(settings, 'ROCKET_CHAT', ROCKET_CHAT)
        return context


class RocketchatIframeAuthView(TemplateView):
    template_name = 'rocketchat.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RocketchatIframeAuthView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RocketchatIframeAuthView, self).get_context_data(**kwargs)
        context['rocketchat'] = getattr(settings, 'ROCKET_CHAT', ROCKET_CHAT)
        return context

    def get(self, request, *argz, **kwargz):
        response = super(RocketchatIframeAuthView, self).get(request, *argz, **kwargz)
        return response

    def post(self, request, *argz, **kwargz):
        origin = request.META.get('HTTP_ORIGIN', '')
        token = request.COOKIES.get('rc_token', '')

        response = HttpResponse(json.dumps({
            'token': token
        }))

        response['Content-Type'] = 'application/json'
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
        response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"

        return response


class AnswerNotificationViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = AnswerNotification.objects.all()
    serializer_class = AnswerNotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'topic'

    def get_queryset(self):
        queryset = super(AnswerNotificationViewSet, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)

        limit_to = self.request.query_params.get('limit_to', None)
        if limit_to:
            queryset = queryset[:int(limit_to)]
        return queryset

    def update(self, request, **kwargs):
        # Find the corresponding AnswerNotification for this call and mark it as read
        try:
            notification = AnswerNotification.objects.get(topic=kwargs.get('topic'), user=request.user)
            notification.is_read = True
            notification.save(skip_date=True)
            return Response(self.get_serializer(notification).data, status=status.HTTP_200_OK)
        except AnswerNotification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            pass


class UnreadNotificationViewSet(viewsets.ModelViewSet):

    queryset = UnreadNotification.objects.all()
    serializer_class = UnreadNotificationSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        # Since the frontend is sending a PUT request to this view, the counter must be reset
        unread = UnreadNotification.objects.get(user=self.request.user)
        unread.counter = 0
        unread.save()
        return Response(self.get_serializer(unread).data)

    def get_queryset(self):
        # If the user is new, a new UnreadNotification must be created
        queryset = UnreadNotification.objects.filter(user=self.request.user)
        if queryset.count() == 0:
            UnreadNotification.objects.create(user=self.request.user)
            queryset = UnreadNotification.objects.filter(user=self.request.user)
        return queryset
