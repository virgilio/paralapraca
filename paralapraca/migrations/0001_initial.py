# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerNotification',
            fields=[
                ('topicnotification_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='discussion.TopicNotification')),
                ('activity', models.ForeignKey(to='activities.Activity')),
            ],
            bases=('discussion.topicnotification',),
        ),
    ]
