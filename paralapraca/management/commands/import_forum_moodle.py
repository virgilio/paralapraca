# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model, models
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification
from django.db import transaction

import unicodecsv
import csv

User = get_user_model()

sizes = {
    'username': 30,
    'last_name': 30,
    'first_name': 30,
}


class Command(BaseCommand):
    args = 'file'
    help = 'import users'

    # Returns the instance of the new forum wich must recieve
    def new_forum(old_forum_id):
        switcher = {
            4: {
                'forum' : '',
                'category' : '',
                'tag': ''
            }
        }

    @transaction.atomic
    def handle(self, *files, **options):

        if not len(files) == 2:
            raise CommandError('Choose two files to import')

        csv.field_size_limit(sys.maxsize) # increase max field size in the csv reader

        # Retrieve the admin superuser
        User = get_user_model()
        me = User.objects.all().first()

        # Create all categories
        catPauta, _ = Category.objects.get_or_create(title='Pautas',description='Pautas',color='FFF')
        catReg, _ = Category.objects.get_or_create(title='Registros',description='Registros',color='FFF')
        catDisc, _ = Category.objects.get_or_create(title='Discussões',description='Discussões',color='FFF')

        # Create all foruns
        fGE, _ = Forum.objects.get_or_create(author=me, title='Fórum Geral')
        fAS, _ = Forum.objects.get_or_create(author=me, title='Fórum Assessoras')
        fNG, _ = Forum.objects.get_or_create(author=me, title='Fórum Natal - Gestão Paralapraca')
        fMG, _ = Forum.objects.get_or_create(author=me, title='Fórum Maracanaú - Gestão Paralapraca')
        fCG, _ = Forum.objects.get_or_create(author=me, title='Fórum Camaçari - Gestão Paralapraca')
        fMG, _ = Forum.objects.get_or_create(author=me, title='Fórum Maracanaú - Gestão Paralapraca')
        fOG, _ = Forum.objects.get_or_create(author=me, title='Fórum Olinda - Gestão Paralapraca')
        fGM, _ = Forum.objects.get_or_create(author=me, title='Fórum Gestão Municipal')


        # The following variable will store every discussion in a dictionary
        topics = {}

        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            count = 0
            for row in readf:
                for fieldname, size in sizes.items():
                    if fieldname in row:
                        row[fieldname] = row[fieldname][:size]



                topics[row['id']] = Topic.objects.create(forum=fGE, title=row['name'], author=me)
                topics[row['id']].categories.add(catPauta)

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

                # If there is no parent, the text message has to be stored in the Topic instance and no Comment instance must be created
                if row['parent'] == '0':
                    disc = topics[row['discussion']]
                    disc.content = row['message']
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

                        # import pdb; pdb.set_trace()
                        comments[row['id']] = Comment.objects.create(
                            topic=topics[row['discussion']],
                            text=row['message'],
                            author=me,
                            parent=parent_comment
                        )
                    else:
                        comments[row['id']] = Comment.objects.create(
                            topic=topics[row['discussion']],
                            text=row['message'],
                            author=me
                        )

                    # TODO adjust user in each comment

                    count += 1
                    if count % 100 == 0:
                        print '.',
