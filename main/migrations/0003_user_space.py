# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170412_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='space',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Space'),
        ),
    ]