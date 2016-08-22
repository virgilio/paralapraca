# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from discussion.models import Topic, Comment, TopicFile, CommentFile
from django.db import transaction
from django.core.files import File as DjangoFile

import unicodecsv
import csv
import sys
import sqlite3

User = get_user_model()


class Command(BaseCommand):
    args = 'file'
    help = 'import users'

    # @transaction.atomic
    def handle(self, *files, **options):

        if not len(files) == 2:
            raise CommandError('Choose one file to import and give the orignal "filedir" path')

        filedir = files[1]

        csv.field_size_limit(sys.maxsize)  # increase max field size in the csv reader

        # Prepare the required tables for migration lookup
        db = sqlite3.connect(':memory:')
        cur = db.cursor()
        cur.execute('''CREATE TABLE bridge (
                        id_moodle INTEGER,
                        id_django INTEGER,
                        topic INTEGER)''')

        # Populate the table with the CSV generated by the import_forum_moodle script
        rdr = csv.reader(open("topicos_migrados.csv"))
        cur.executemany('''
            INSERT INTO bridge (id_moodle, id_django, topic)
                VALUES (?,?, '1')''', rdr)

        rdr = csv.reader(open("comentarios_migrados.csv"))
        cur.executemany('''
            INSERT INTO bridge (id_moodle, id_django, topic)
                VALUES (?,?, '0')''', rdr)

        db.commit()

        # Read all the attachments data used by Moodle
        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            for row in readf:
                if row['filename'] == '.':
                    print("skipped: " + row['filename'])
                    continue  # If there is no valid filename data in the moodle table, this file must be skipped

                # Check if the current attachment belongs to a imported topic or comment
                cur = db.cursor()
                cur.execute("SELECT id_django FROM bridge WHERE id_moodle = '" + row['itemid'] + "' AND topic = 1")
                id_django = cur.fetchone()

                # Tries to find a matching topic
                if id_django and Topic.objects.filter(id=id_django[0]):

                    # Find the file
                    file_path = '{0}/{1}/{2}/{3}'.format(filedir, row['contenthash'][0:2], row['contenthash'][2:4], row['contenthash'])  # the target file path created by moodle

                    with open(file_path, 'r') as file:
                        topic = Topic.objects.get(id=id_django[0])
                        attachment = TopicFile.objects.create(
                            name=row['filename'],
                            topic=topic,
                            file=DjangoFile(file)
                        )

                    # Attach the file to the topic
                    topic.files.add(attachment)
                    topic.save()
                    print(".")

                else:
                    cur = db.cursor()
                    cur.execute("SELECT id_django FROM bridge WHERE id_moodle = '" + row['itemid'] + "' AND topic = 0")
                    id_django = cur.fetchone()
                    # Tries to find a matching comment
                    if id_django and Comment.objects.filter(id=id_django[0]):

                        # Find the file
                        file_path = '{0}/{1}/{2}/{3}'.format(filedir, row['contenthash'][0:2], row['contenthash'][2:4], row['contenthash'])  # the target file path created by moodle

                        comment = Comment.objects.get(id=id_django[0])
                        attachment = CommentFile.objects.create(
                            name=row['filename'],
                            comment=comment,
                            file=file_path
                        )

                        # Attach the file to the topic
                        comment.files.add(attachment)
                        comment.save()
                        print(".")
