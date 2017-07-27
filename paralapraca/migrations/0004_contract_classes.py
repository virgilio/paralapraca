# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20170125_1147'),
        ('paralapraca', '0003_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='classes',
            field=models.ManyToManyField(related_name='contracts', to='core.Class'),
        ),
    ]
