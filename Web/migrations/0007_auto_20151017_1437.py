# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0006_auto_20151010_1904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='createapplication',
            options={'ordering': ['-submission_time']},
        ),
        migrations.AlterModelOptions(
            name='deleteapplication',
            options={'ordering': ['-submission_time']},
        ),
        migrations.AlterModelOptions(
            name='portapplication',
            options={'ordering': ['-submission_time']},
        ),
        migrations.AlterField(
            model_name='createapplication',
            name='os',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='machineinfo',
            name='last_connect_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='portapplication',
            name='review_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
