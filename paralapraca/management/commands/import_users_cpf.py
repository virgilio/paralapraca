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

    def handle(self, *files, **options):

        if not len(files) == 1:
            raise CommandError('No file to import')

        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            for row in readf:
                try:
                    email = row.pop('email')
                    cpf = row.pop('cpf')
                    user = User.objects.get(email__contains=email)
                    user.cpf = cpf
                    user.save()
                except Exception as e:
                    print(e)
                    print(email)
                    print('\n\n')
