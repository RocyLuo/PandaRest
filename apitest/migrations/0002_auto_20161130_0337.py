# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 03:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='parent_id',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='apitest.Catalog'),
        ),
    ]
