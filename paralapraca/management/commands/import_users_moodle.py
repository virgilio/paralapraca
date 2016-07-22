# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model, models
from django.db import transaction
from django.db.models import Q

import unicodecsv


User = get_user_model()

sizes = {
    'username': 30,
    'last_name': 30,
    'first_name': 30,
}


class Command(BaseCommand):
    args = 'file'
    help = 'import users'

    @transaction.atomic
    def handle(self, *files, **options):

        if not len(files) == 1:
            raise CommandError('Choose a file to import')

        # This file comes from moodle's DB and generates only deactivated users
        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            count = 0
            for row in readf:
                for fieldname, size in sizes.items():
                    if fieldname in row:
                        row[fieldname] = row[fieldname][:size]

                user, created = User.objects.get_or_create(email=row['email'][:29])
                if user.username != row['username'][:29] and not User.objects.filter(username=row['username'][:29]).exists():
                    user.username = row['username'][:29]
                else:
                    user.username = row['email'][:29].split('@')[0]
                    print(row['email'][:29].split('@')[0])

                user.first_name = row['firstname'][:29]
                user.last_name = row['lastname'][:29]
                user.city = row['city'][:29]
                user.is_active = False
                user.accepted_terms = False
                user.save()
