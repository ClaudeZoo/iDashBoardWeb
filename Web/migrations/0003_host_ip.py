# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0002_auto_20150926_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='ip',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
