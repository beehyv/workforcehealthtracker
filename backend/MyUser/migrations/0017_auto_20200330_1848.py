# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-03-30 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0016_resultstatus_result_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultstatus',
            name='result_message',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Result message'),
        ),
    ]