# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0008_host_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vm',
            name='nat_rules',
            field=models.TextField(default=b'[]', null=True),
        ),
    ]
