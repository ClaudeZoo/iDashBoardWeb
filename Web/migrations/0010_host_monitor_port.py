# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0009_auto_20151018_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='monitor_port',
            field=models.IntegerField(null=True),
        ),
    ]
