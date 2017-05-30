# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('paralapraca', '0002_unreadnotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=128, unique=True, verbose_name='Slug')),
                ('unities', django.contrib.postgres.fields.ArrayField(help_text='Possibly cities. This field stores the user declared unities on contract creation. This are used to distinguish some special grupos associated to the contract', base_field=models.CharField(max_length=255, blank=True), size=None)),
                ('groups', models.ManyToManyField(help_text='Groups created to enforce this contract restrictions in several other models', related_name='contracts', verbose_name='groups', to='auth.Group', blank=True)),
            ],
            options={
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
            },
        ),
    ]
