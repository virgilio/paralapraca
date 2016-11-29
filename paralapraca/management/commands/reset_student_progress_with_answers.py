# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Unit, StudentProgress
from activities.models import Answer, Activity


class Command(BaseCommand):
    help = 'Search for instances of StudentProgress connected to Activities of the type discussion and reset its "complete" field based on the existence of an corresponding Answer instance'

    @transaction.atomic
    def handle(self, *files, **options):

        activities_discussion = Activity.objects.filter(type='discussion')

        units_discussion = Unit.objects.filter(activities=activities_discussion)

        answers_discussion = Answer.objects.filter(activity=activities_discussion)

        progress_discussion = StudentProgress.objects.filter(unit=units_discussion)

        for progress in progress_discussion:
            my_answer = answers_discussion.filter(user=progress.user, activity__unit__progress=progress)
            if my_answer.count() == 0 and progress.complete is not None:
                # This progress is incorrectly saved and must be corrected now
                progress.complete = None
                progress.save()
