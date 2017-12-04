# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paralapraca', '0004_contract_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='classes',
            field=models.ManyToManyField(related_name='contract', to='core.Class'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='groups',
            field=models.ManyToManyField(help_text='Groups created to enforce this contract restrictions in several other models', related_name='contract', verbose_name='groups', to='auth.Group', blank=True),
        ),
    ]
