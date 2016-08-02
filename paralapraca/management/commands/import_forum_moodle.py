# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from discussion.models import Group, Category, Forum, Topic, Comment, Tag
from django.db import transaction
from django.utils import timezone

import unicodecsv
import csv
import sys
import datetime

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

        if not len(files) == 2:
            raise CommandError('Choose two files to import')

        csv.field_size_limit(sys.maxsize)  # increase max field size in the csv reader

        # Retrieve the admin superuser
        User = get_user_model()

        # Create all categories
        catPauta, _ = Category.objects.get_or_create(name='Pautas', description='Pautas', color='FFF')
        catReg, _ = Category.objects.get_or_create(name='Registros', description='Registros', color='FFF')
        catDisc, _ = Category.objects.get_or_create(name='Discussões', description='Discussões', color='FFF')

        # Create all foruns
        fGE, _ = Forum.objects.get_or_create(title='Fórum Geral')
        fAS, _ = Forum.objects.get_or_create(title='Fórum Assessoras')
        fNG, _ = Forum.objects.get_or_create(title='Fórum Natal - Gestão Paralapraca')
        fMG, _ = Forum.objects.get_or_create(title='Fórum Maracanaú - Gestão Paralapraca')
        fCG, _ = Forum.objects.get_or_create(title='Fórum Camaçari - Gestão Paralapraca')
        fMG, _ = Forum.objects.get_or_create(title='Fórum Maracanaú - Gestão Paralapraca')
        fOG, _ = Forum.objects.get_or_create(title='Fórum Olinda - Gestão Paralapraca')
        fGM, _ = Forum.objects.get_or_create(title='Fórum Gestão Municipal')

        # Forum Geral is marked as public by default
        fGE.is_public = True
        fGE.save()

        # Create the nedded tags for the migrations
        tOrg, _ = Tag.objects.get_or_create(name='Organização de Ambiente')
        tArt, _ = Tag.objects.get_or_create(name='Artes Visuais')
        tPai, _ = Tag.objects.get_or_create(name='Paisagens Culturais')
        tBri, _ = Tag.objects.get_or_create(name='Brincar')
        tExp, _ = Tag.objects.get_or_create(name='Exploração de Mundo')
        tLit, _ = Tag.objects.get_or_create(name='Literatura')
        tMus, _ = Tag.objects.get_or_create(name='Música')

        # Test if the user groups have already been created
        if not Group.objects.filter(name='Avante'):
            print("Import users and their groups before running this script.")
            sys.exit()

        # Get every possible group in wich users can be put in
        gAv = Group.objects.get(name='Avante')
        gEn = Group.objects.get(name='Entremeios')
        gAs = Group.objects.get(name='Assessoras')

        # Assign groups to its respectives forums
        # Forum Assessoras
        fAS.groups.add(gAs, gAv, gEn)

        # Holds all the necesseary exchange info for each source and destination forum in the migration
        exchange = {
            4: {
                'forum': fGE,
                'category': catDisc,
            },
            15: {
                'forum': fAS,
            },
            27: {
                'forum': fGE,
                'category': catReg,
                'tag': tOrg,
            },
            22: {
                'forum': fGE,
                'category': catReg,
                'tag': tArt,
            },
            7: {
                'forum': fGE,
                'category': catPauta,
            },
            5: {
                'forum': fGE,
                'category': catReg,
                'tag': tPai,
            },
            23: {
                'forum': fGE,
                'category': catReg,
                'tag': tBri,
            },
            25: {
                'forum': fGE,
                'category': catReg,
                'tag': tExp,
            },
            6: {
                'forum': fGE,
                'category': catReg,
            },
            18: {
                'forum': fGE,
                'category': catPauta,
                'tag': tLit,
            },
            26: {
                'forum': fGE,
                'category': catReg,
                'tag': tMus,
            },
            20: {
                'forum': fGE,
                'category': catPauta,
                'tag': tMus,
            },
            8: {
                'forum': fGE,
                'category': catPauta,
                'category2': catReg,
            },
            16: {
                'forum': fGE,
                'category': catPauta,
                'tag': tArt,
            },
            52: {
                'forum': fGE,
            },
            21: {
                'forum': fCG,
            },
            47: {
                'forum': fGM,
            },
            51: {
                'forum': fGE,
                'category': catPauta,
                'tag': tBri,
            },
            17: {
                'forum': fGE,
                'category': catPauta,
                'tag': tExp,
            },
            43: {
                'forum': fMG,
            },
        }

        # The following variable will store every discussion in a dictionary
        topics = {}

        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            count = 0
            for row in readf:
                for fieldname, size in sizes.items():
                    if fieldname in row:
                        row[fieldname] = row[fieldname][:size]

                # Find out wich forum is the corret one for the current topic
                destination = exchange.get(int(row['forum']))

                last_activity_at = timezone.make_aware(
                    datetime.datetime.fromtimestamp(
                        float(
                            row['timemodified']
                        )
                    ),
                    timezone.get_current_timezone()
                )

                topics[row['id']] = Topic.objects.create(
                    forum=destination['forum'],
                    title=row['name'].encode('utf-8'),
                    author=User.objects.get(email=row['email']),
                    last_activity_at=last_activity_at,
                    created_at=last_activity_at,
                    updated_at=last_activity_at,
                )

                # TODO: store new and old topic id in a csv for future reference

                # Add all categories relevant to this topic1
                if 'category' in destination:
                    topics[row['id']].categories.add(destination['category'])
                    if 'category2' in destination:
                        topics[row['id']].categories.add(destination['category2'])

                # Add all tags relevant to this topic
                if 'tag' in destination:
                    topics[row['id']].tags.add(destination['tag'])

                count += 1
                if count % 100 == 0:
                    print '.',

        with open(files[1], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            count = 0

            # This variable will keep track of all comments added.
            # This will be useful for assigning parent comments when nedded
            comments = {}

            for row in readf:
                for fieldname, size in sizes.items():
                    if fieldname in row:
                        row[fieldname] = row[fieldname][:size]

                # Adjusts the created and modified dates to the Django standard
                # TODO: use django packages to retrieve the timezone
                created = timezone.make_aware(
                    datetime.datetime.fromtimestamp(
                        float(
                            row['created']
                        )
                    ),
                    timezone.get_current_timezone()
                )

                modified = timezone.make_aware(
                    datetime.datetime.fromtimestamp(
                        float(
                            row['modified']
                        )
                    ),
                    timezone.get_current_timezone()
                )

                # If there is no parent, the text message has to be stored in the Topic instance and no Comment instance must be created
                if row['parent'] == '0':
                    disc = topics[row['discussion']]
                    disc.content = row['message']
                    disc.created_at = created
                    disc.updated_at = modified
                    disc.save()

                else:
                    # If we got here, the current comment has another comment as a parent
                    # Now, we must resolve the parent id to the first comment in the nesting tree
                    # This is nedded since Moodle allows unlimited nesting and django_discussion allows only one
                    if row['parent'] in comments.keys():

                        # Is this child comment in the first level?
                        if comments[row['parent']].parent:
                            # If it is not, the parent of its parent will be used
                            parent_comment = comments[row['parent']].parent
                        else:
                            # If it is, the parent can be safely used
                            parent_comment = comments[row['parent']]

                        comments[row['id']] = Comment.objects.create(
                            topic=topics[row['discussion']],
                            text=row['message'],
                            author=User.objects.get(email=row['email']),
                            parent=parent_comment,
                            created_at=created,
                            updated_at=modified,
                        )
                    else:
                        comments[row['id']] = Comment.objects.create(
                            topic=topics[row['discussion']],
                            text=row['message'],
                            author=User.objects.get(email=row['email']),
                            created_at=created,
                            updated_at=modified,
                        )

                    count += 1
                    if count % 100 == 0:
                        print '.',

                    # TODO: store new and old comment id in a csv for future reference
