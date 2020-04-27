# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-03-26 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0007_hcworker_result_status_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hcwtype',
            options={'verbose_name': 'Health Care Worker Type'},
        ),
        migrations.AlterField(
            model_name='hcworker',
            name='result_status_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MyUser.ResultStatus'),
        ),
    ]