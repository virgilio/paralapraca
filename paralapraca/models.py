# -*- coding: utf-8 -*-
from django.db import models
from discussion.models import TopicNotification
from activities.models import Activity


class AnswerNotification(TopicNotification):

    activity = models.ForeignKey(Activity)
