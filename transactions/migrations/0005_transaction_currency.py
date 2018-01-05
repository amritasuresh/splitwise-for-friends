# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-05 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_merge_20171105_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='currency',
            field=models.CharField(choices=[('EUR', 'EURO'), ('USD', 'US DOLLAR'), ('PLN', 'POLISH ZLOTY'), ('INR', 'INDIAN RUPEE')], default='EUR', max_length=3),
        ),
    ]