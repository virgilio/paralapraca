# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paralapraca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnreadNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.IntegerField(null=True, blank=True)),
                ('user', models.OneToOneField(verbose_name=b'user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
