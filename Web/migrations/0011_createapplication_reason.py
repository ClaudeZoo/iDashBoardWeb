# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0010_host_monitor_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='createapplication',
            name='reason',
            field=models.TextField(max_length=100, null=True),
        ),
    ]
