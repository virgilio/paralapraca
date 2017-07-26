# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.models import CourseStudent, Class
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "All enrolled students should be members of a class. This scripts finds any incosistent profiles that don't match that condition"

    def handle(self, *files, **options):
        users = []
        for cs in CourseStudent.objects.all():
            try:
                Class.objects.get(course=cs.course, students__in=[cs.user])
            except Class.DoesNotExist as e:
                users.append([cs.user, cs.course])
        print(users)
