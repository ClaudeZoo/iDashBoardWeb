# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vm',
            old_name='vmHost',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='vmName',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='vmUser',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='machineinfo',
            name='state',
        ),
        migrations.RemoveField(
            model_name='machineinfo',
            name='type',
        ),
        migrations.AddField(
            model_name='host',
            name='vm_manager_port',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='operationrecord',
            name='information',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='portapplication',
            name='protocol',
            field=models.TextField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='state',
            field=models.CharField(default='deleted', max_length=10),
            preserve_default=False,
        ),
    ]
