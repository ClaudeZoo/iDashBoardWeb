# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
                ('review_time', models.DateTimeField(null=True)),
                ('vm_type', models.TextField(null=True)),
                ('os', models.TextField(null=True)),
                ('host_name', models.CharField(max_length=20, null=True)),
                ('user_name', models.TextField(max_length=30, null=True)),
                ('password', models.TextField(null=True)),
                ('memory', models.IntegerField(null=True)),
                ('state', models.CharField(max_length=10)),
                ('error', models.TextField(null=True)),
                ('applicant', models.ForeignKey(related_name='my_create_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeleteApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
                ('review_time', models.DateTimeField(null=True)),
                ('state', models.CharField(max_length=10)),
                ('error', models.TextField(null=True)),
                ('applicant', models.ForeignKey(related_name='my_delete_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=100, null=True)),
                ('phone', models.PositiveIntegerField(null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('free_ports', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MachineInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wan_ip', models.TextField(null=True)),
                ('lan_ip', models.TextField(null=True)),
                ('ssh_port', models.PositiveIntegerField(null=True)),
                ('type', models.PositiveIntegerField(null=True)),
                ('state', models.TextField(null=True)),
                ('last_connect_time', models.DateTimeField(auto_now=True)),
                ('state_info', models.TextField(null=True)),
                ('inet4', models.TextField(null=True)),
                ('broadcast', models.TextField(null=True)),
                ('inet6', models.TextField(null=True)),
                ('mask', models.TextField(null=True)),
                ('dns', models.TextField(null=True)),
                ('users', models.TextField(null=True)),
                ('load_average', models.TextField(null=True)),
                ('tasks', models.TextField(null=True)),
                ('percent_cpu', models.TextField(null=True)),
                ('memory', models.TextField(null=True)),
                ('swap', models.TextField(null=True)),
                ('process', models.TextField(null=True)),
                ('hostname', models.TextField(null=True)),
                ('username', models.TextField(null=True)),
                ('cpu_info', models.TextField(null=True)),
                ('os_info', models.TextField(null=True)),
                ('disk', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperationRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=10)),
                ('execute_time', models.DateTimeField(auto_now_add=True)),
                ('result', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(related_name='my_operations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PortApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vm_port', models.IntegerField()),
                ('host_port', models.IntegerField()),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
                ('review_time', models.DateTimeField(null=True)),
                ('state', models.CharField(max_length=10)),
                ('error', models.TextField(null=True)),
                ('applicant', models.ForeignKey(related_name='my_port_applications', to=settings.AUTH_USER_MODEL)),
                ('host', models.ForeignKey(to='Web.Host')),
                ('reviewer', models.ForeignKey(related_name='port_applications', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.TextField(null=True)),
                ('vmName', models.TextField(null=True)),
                ('nat_rules', models.TextField(null=True)),
                ('info', models.OneToOneField(to='Web.MachineInfo')),
                ('vmHost', models.ForeignKey(related_name='vms', to='Web.Host', null=True)),
                ('vmUser', models.ForeignKey(related_name='my_vms', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='portapplication',
            name='vm',
            field=models.ForeignKey(to='Web.VM'),
        ),
        migrations.AddField(
            model_name='operationrecord',
            name='vm',
            field=models.ForeignKey(related_name='vm_record', to='Web.VM'),
        ),
        migrations.AddField(
            model_name='host',
            name='info',
            field=models.OneToOneField(to='Web.MachineInfo'),
        ),
        migrations.AddField(
            model_name='deleteapplication',
            name='host',
            field=models.ForeignKey(to='Web.Host'),
        ),
        migrations.AddField(
            model_name='deleteapplication',
            name='reviewer',
            field=models.ForeignKey(related_name='delete_applications', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='deleteapplication',
            name='vm',
            field=models.ForeignKey(to='Web.VM'),
        ),
        migrations.AddField(
            model_name='createapplication',
            name='host',
            field=models.ForeignKey(to='Web.Host', null=True),
        ),
        migrations.AddField(
            model_name='createapplication',
            name='reviewer',
            field=models.ForeignKey(related_name='create_applications', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='createapplication',
            name='vm',
            field=models.ForeignKey(to='Web.VM', null=True),
        ),
    ]
