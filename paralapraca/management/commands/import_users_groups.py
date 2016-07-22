# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model, models
from django.contrib.auth.models import Group
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

        # Create or get every possible group in wich users can be put in
        gAv, _ = Group.objects.get_or_create(name='Avante')
        gEn, _ = Group.objects.get_or_create(name='Entremeios')
        gAs, _ = Group.objects.get_or_create(name='Assessoras')
        gDu, _ = Group.objects.get_or_create(name='Duplas')
        gCo, _ = Group.objects.get_or_create(name='Coordenadoras')
        gGe, _ = Group.objects.get_or_create(name='Gestores')
        gCa, _ = Group.objects.get_or_create(name='Camaçari')
        gMac, _ = Group.objects.get_or_create(name='Maceió')
        gMar, _ = Group.objects.get_or_create(name='Maracanaú')
        gOl, _ = Group.objects.get_or_create(name='Olinda')
        gNa, _ = Group.objects.get_or_create(name='Natal')

        # This file specifies wich users must be activated and in wich groups they must be put
        # Only one file is expected, but this operation can be repeated for several files
        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            for row in readf:
                for fieldname, size in sizes.items():
                    if fieldname in row:
                        row[fieldname] = row[fieldname][:size]

                # Find out if the user being currently imported already is in the database
                # Email is considered a suitable key for this task
                if User.objects.filter(email=row['email'][:29]).exists():
                    user = User.objects.get(email=row['email'][:29])
                    if row['remocao'] == '1':
                        # deactivate this user's profile
                        user.is_active = False
                        user.save()
                        print("User "+row['email'][:29]+" has been deactivated.\n")
                    else:
                        # put this user in the specified group
                        group = row.pop('grupo')
                        user.groups.add(Group.objects.get(name=group))
                        user.is_active = True
                        user.save()
                else:
                    # If the user can't be found, it must be created
                    # TODO create the new username based on the first words of its names
                    nu = User.objects.create(
                        username=row['email'][:29], # django has a 30 char limitation in the following fields
                        first_name=row['username'].split(' ', 1)[0][:29],
                        last_name=row['username'].split(' ', 1)[1][:29],
                        email=row['email'][:29],
                    )
                    nu.is_active = True
                    nu.accepted_terms = False
                    nu.save()

                    print("User "+row['email'][:29]+" couldn't be found in the database and has been created.\n")
