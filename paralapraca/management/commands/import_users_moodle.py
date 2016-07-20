# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model, models
from django.db import transaction

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

                # set_password = row.pop('password')

                nu = User.objects.create(
                    username=row['username'][:29], # django has a 30 char limitation in the following fields
                    first_name=row['firstname'][:29],
                    last_name=row['lastname'][:29],
                    email=row['email'][:29],
                    city=row['city'][:29],
                    biography=row['description'],
                )
                # nu.set_password(set_password)
                nu.is_active = False
                nu.accepted_terms = False
                nu.save()
