# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0003_host_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='vm',
            name='memory',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='os',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='vm_type',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='createapplication',
            name='os',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='createapplication',
            name='review_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='createapplication',
            name='vm_type',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='deleteapplication',
            name='review_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='machineinfo',
            name='last_connect_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
