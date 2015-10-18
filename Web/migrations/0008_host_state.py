# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0007_auto_20151017_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='state',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
