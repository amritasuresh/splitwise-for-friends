# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-10 05:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Currency',
        ),
    ]
