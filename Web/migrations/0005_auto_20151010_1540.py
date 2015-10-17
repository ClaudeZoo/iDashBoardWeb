# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0004_auto_20151010_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vm',
            name='state',
            field=models.CharField(max_length=15),
        ),
    ]
