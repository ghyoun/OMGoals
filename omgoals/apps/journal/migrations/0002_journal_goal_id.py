# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('add_goal', '0003_auto_20160630_1847'),
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='goal_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='add_goal.Goal'),
            preserve_default=False,
        ),
    ]
