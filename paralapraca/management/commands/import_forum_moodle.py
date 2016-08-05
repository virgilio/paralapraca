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

csv.register_dialect(
    'dialeto',
    delimiter=',',
    quotechar='"',
    doublequote=True,
    skipinitialspace=True,
    lineterminator='\r\n',
    quoting=csv.QUOTE_MINIMAL)


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
        catDisc, _ = Category.objects.get_or_create(name='Discussões'.decode('utf-8'), description='Discussões'.decode('utf-8'), color='FFF')

        # Create all foruns
        fGE, _ = Forum.objects.get_or_create(title='Fórum Geral'.decode('utf-8'))
        fAS, _ = Forum.objects.get_or_create(title='Fórum Assessoras'.decode('utf-8'))
        fNG, _ = Forum.objects.get_or_create(title='Fórum Natal - Assessoras'.decode('utf-8'))
        fMG, _ = Forum.objects.get_or_create(title='Fórum Maracanaú - Assessoras'.decode('utf-8'))
        fCG, _ = Forum.objects.get_or_create(title='Fórum Camaçari - Assessoras'.decode('utf-8'))
        fMA, _ = Forum.objects.get_or_create(title='Fórum Maceió - Assessoras'.decode('utf-8'))
        fOG, _ = Forum.objects.get_or_create(title='Fórum Olinda - Assessoras'.decode('utf-8'))
        fGM, _ = Forum.objects.get_or_create(title='Fórum Geral - Gestão Municipal'.decode('utf-8'))

        fNGest, _ = Forum.objects.get_or_create(title='Fórum Natal Gestores'.decode('utf-8'))
        fCGest, _ = Forum.objects.get_or_create(title='Fórum Camaçari Gestores'.decode('utf-8'))
        fOGest, _ = Forum.objects.get_or_create(title='Fórum Olinda Gestores'.decode('utf-8'))
        fMarGest, _ = Forum.objects.get_or_create(title='Fórum Marcanaú Gestores'.decode('utf-8'))
        fMacGest, _ = Forum.objects.get_or_create(title='Fórum Maceió Gestores'.decode('utf-8'))

        # Create the nedded tags for the migrations
        tOrg, _ = Tag.objects.get_or_create(name='Organização de Ambiente'.decode('utf-8'))
        tArt, _ = Tag.objects.get_or_create(name='Artes Visuais'.decode('utf-8'))
        tPai, _ = Tag.objects.get_or_create(name='Paisagens Culturais'.decode('utf-8'))
        tBri, _ = Tag.objects.get_or_create(name='Brincar'.decode('utf-8'))
        tExp, _ = Tag.objects.get_or_create(name='Exploração de Mundo'.decode('utf-8'))
        tLit, _ = Tag.objects.get_or_create(name='Literatura'.decode('utf-8'))
        tMus, _ = Tag.objects.get_or_create(name='Música'.decode('utf-8'))

        # Test if the user groups have already been created
        if not Group.objects.filter(name='Avante'):
            print("Import users and their groups before running this script.")
            sys.exit()

        # Get relevant groups in wich users can be put in
        gAv = Group.objects.get(name='Avante')
        gEn = Group.objects.get(name='Entremeios')
        gAs = Group.objects.get(name='Assessoras')
        gDu = Group.objects.get(name='Duplas')
        gCo = Group.objects.get(name='Coordenadoras')
        gGe = Group.objects.get(name='Gestores')
        gCa = Group.objects.get(name=u'Camaçari')
        gMac = Group.objects.get(name=u'Maceió')
        gMar = Group.objects.get(name=u'Maracanaú')
        gOl = Group.objects.get(name='Olinda')
        gNa = Group.objects.get(name='Natal')

        gAN = Group.objects.get(name='Assessoras Natal')
        gAC = Group.objects.get(name=u'Assessoras Camaçari')
        gAO = Group.objects.get(name='Assessoras Olinda')
        gAM = Group.objects.get(name=u'Assessoras Maracanaú')
        gAMc = Group.objects.get(name=u'Assessoras Maceió')

        gGestN = Group.objects.get(name='Gestores Natal')
        gGestC = Group.objects.get(name=u'Gestores Camaçari')
        gGestO = Group.objects.get(name='Gestores Olinda')
        gGestMar = Group.objects.get(name=u'Gestores Maracanaú')
        gGestMac = Group.objects.get(name=u'Gestores Maceió')

        # Assign groups to its respectives forums
        # Forum Geral
        fGE.groups.add(gAv, gEn, gAs, gDu, gCo, gCa, gMac, gMar, gOl, gNa, gAN, gAC, gAO, gAM, gAMc, gGestN, gGestC, gGestO, gGestMar, gGestMac)

        # Forum Assessoras
        fAS.groups.add(gAs, gAv, gEn)

        # Forum Natal Assessoras
        fNG.groups.add(gAN, gAv, gEn)

        # Forum Camaçari Assessoras
        fCG.groups.add(gAC, gAv, gEn)

        # Forum Olinda Assessoras
        fOG.groups.add(gAO, gAv, gEn)

        # Fórum Maracanaú Assessoras
        fMG.groups.add(gAM, gAv, gEn)

        # Fórum Maceió Assessoras
        fMA.groups.add(gAMc, gAv, gEn)

        # Fórum Geral - Gestão Municipal
        fGM.groups.add(gGe, gAv, gEn)

        # Fórum Natal Gestores
        fNGest.groups.add(gGestN, gAv, gEn)

        # Fórum Camaçari Gestores
        fCGest.groups.add(gGestC, gAv, gEn)

        # Fórum Olinda Gestores
        fOGest.groups.add(gGestO, gAv, gEn)

        # Fórum Maracanaú Gestores
        fMarGest.groups.add(gGestMar, gAv, gEn)

        # Fórum Maceió Gestores
        fMacGest.groups.add(gGestMac, gAv, gEn)

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

        # Prepare the data for csv archiving
        topics_csv = []
        topics_csv.append(['id_moodle', 'id_django'])
        comments_csv = []
        comments_csv.append(['id_moodle', 'id_django'])

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
                    title=row['name'],
                    author=User.objects.get(email=row['email']),
                    last_activity_at=last_activity_at,
                    created_at=last_activity_at,
                    updated_at=last_activity_at,
                )

                # Store new and old topic id in a csv for future reference
                topics_csv.append([row['id'], topics[row['id']].id])

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

        # Now that all the topics have been writeen in the Django database,
        # we must store the association data in a csv file
        with open('topicos_migrados.csv', 'w') as file:
            w = csv.writer(file, dialect='dialeto')
            for row in topics_csv:
                w.writerow(row)

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

                    # Store new and old comment id in a csv for future reference
                    comments_csv.append([row['id'], comments[row['id']].id])

                    count += 1
                    if count % 100 == 0:
                        print '.',

        # Now that all the comments have been writeen in the Django database,
        # we must store the association data in a csv file
        with open('comentarios_migrados.csv', 'w') as file:
            w = csv.writer(file, dialect='dialeto')
            for row in comments_csv:
                w.writerow(row)
