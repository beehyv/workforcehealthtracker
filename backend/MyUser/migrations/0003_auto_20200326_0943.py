# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-26 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0002_auto_20200326_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='whatsapp_number',
            field=models.CharField(blank=True, default=0, max_length=10, null=True, verbose_name='Whatsapp Number'),
        ),
    ]