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
from paralapraca.models import AnswerNotification, UnreadNotification, Contract
from core.models import Course, CourseStudent
from accounts.models import TimtecUser
from paralapraca.serializers import AnswerNotificationSerializer, UnreadNotificationSerializer, UserInDetailSerializer, UsersByClassSerializer, ContractSerializer
from discussion.models import Comment, CommentLike, Topic, TopicLike
from rest_pandas import PandasViewSet
from rest_pandas.renderers import PandasCSVRenderer, PandasJSONRenderer
import pandas as pd


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


class ContractViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


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


class SummaryViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        statistics_per_course = [
            {'name': course.name,
             'user_count': course.coursestudent_set.count(),
             'user_finished_course_count': [student.can_emmit_receipt() for student in course.coursestudent_set.all()].count(True),
             'classes': [
                {'name': klass.name,
                 'user_count': klass.get_students.count(),
                 'certificate_count': [cs.certificate.type for cs in klass.get_students.all()].count('certificate')
                } for klass in course.class_set.all()]
            } for course in Course.objects.all()
        ]
        return Response({
            'user_count': TimtecUser.objects.count(),
            'total_number_of_topics': Topic.objects.count(),
            'total_number_of_comments': Comment.objects.count(),
            'total_number_of_likes': TopicLike.objects.count() + CommentLike.objects.count(),
            'statistics_per_course': statistics_per_course})


class UsersByGroupViewSet(PandasViewSet):

    permission_classes = [IsAuthenticated]
    renderer_classes = [PandasCSVRenderer, PandasJSONRenderer]
    queryset = TimtecUser.objects.all()

    def list(self, request, format=None):
        groups = request.query_params.get('group', None)
        if groups is not None:
            serializer = UserInDetailSerializer(self.queryset.filter(groups__name__in=groups.split(',')), many=True)
        else:
            serializer = UserInDetailSerializer(self.queryset, many=True)
        # in order to get the data in the wanted column form, I'll need to make some transformations
        return Response(self.transform_data(serializer.data))

    def transform_data(self, data):
        response = []
        for user in data:
            for course in user.get('courses'):
                user.update({
                    u'{} - progresso'.format(course['course_name']): course['percent_progress'],
                    u'{} - nome da turma'.format(course['course_name']): course['class_name'],
                    u'{} - possui certificado'.format(course['course_name']): course['has_certificate']
                })
            user.pop('courses', None)
            response.append(user)
        return pd.DataFrame.from_dict(response)


class UsersByClassViewSet(PandasViewSet):

    permission_classes = [IsAuthenticated]
    queryset = CourseStudent.objects.all()

    def list(self, request, format=None):
        ids = request.query_params.get('id', None)
        if ids is not None:
            # This is a bit ugly, but should work. There is no (easy) way to directly filter from
            # a function, so I'm getting all the desired IDs, then filtering by the desired IDs
            ids = ids.split(',')
            ids = [int(idt) for idt in ids]
            cs_ids = []
            for x in self.queryset:
                try:
                    if x.get_current_class().id in ids:
                        cs_ids.append(x.id)
                except Exception as e:
                    # If no class has been found, pass the error silently
                    pass

            serializer = UsersByClassSerializer(self.queryset.filter(id__in=cs_ids), many=True)
        else:
            serializer = UsersByClassSerializer(self.queryset, many=True)
        return Response(pd.DataFrame.from_dict(self.transform_data(serializer.data)).set_index('cpf'))

    def transform_data(self, data):
        for coursestudent in data:
            for lesson in coursestudent.get(u'percent_progress_by_lesson', None):
                coursestudent.update({
                    u'Lição {} - Progresso'.format(lesson['name']): lesson['progress']
                })
                for activity in lesson.get(u'activities', None):
                    coursestudent.update({
                        u'Lição {} - Atividade {} realizada'.format(lesson['name'], activity['name']): activity['done']
                    })
            coursestudent.pop('percent_progress_by_lesson', None)
        return data
