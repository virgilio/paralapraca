# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import StudentProgress
from django.utils import timezone


class Command(BaseCommand):
    help = 'Mark every pending activity from students as complete with the current timestamp. Beaware that only StudentProgress instances that have already been created and are not yet marked as completed can be affected '

    @transaction.atomic
    def handle(self, *files, **options):

        incomplete_progress = StudentProgress.objects.filter(complete=None)
        for prg in incomplete_progress:
            prg.complete = timezone.now()
            prg.save()
