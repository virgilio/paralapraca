# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from discussion.models import TopicNotification
from activities.models import Activity


class AnswerNotification(TopicNotification):

    activity = models.ForeignKey(Activity)


class UnreadNotification(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='user', on_delete=models.CASCADE)
    counter = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # This is a new unread counter
            # All AnswerNotification and TopicNotification will be used to create the first unread counter for this user
            # However, counting only the unread TopicNotification instances is enough, since every AnswerNotification also has a row in the TopicNotification table
            self.counter = TopicNotification.objects.filter(
                user=self.user,
                is_read=False).count()
        super(UnreadNotification, self).save(*args, **kwargs)
