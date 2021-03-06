# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 05:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
        ('groups', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('TC', 'TRANSACTION CREATED'), ('TF', 'TRANSACTION FINISHED'), ('GA', 'ADDED TO GROUP')], max_length=2)),
                ('accounts', models.ManyToManyField(to='accounts.Account')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='groups.UserGroup')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transactions.Transaction')),
            ],
        ),
    ]
