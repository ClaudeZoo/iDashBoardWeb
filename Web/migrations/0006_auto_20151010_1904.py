# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0005_auto_20151010_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='free_ports',
            new_name='ports_info',
        ),
    ]
