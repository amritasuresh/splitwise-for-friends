# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 04:02
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('name', models.CharField(max_length=150)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('message', models.TextField()),
            ],
        ),
    ]
