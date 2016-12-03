# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 09:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0019_auto_20161202_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cataloghaschunk',
            name='catalog',
        ),
        migrations.RemoveField(
            model_name='cataloghaschunk',
            name='chunk',
        ),
        migrations.RemoveField(
            model_name='dboperation',
            name='chunk',
        ),
        migrations.RemoveField(
            model_name='requestoperation',
            name='chunk',
        ),
        migrations.DeleteModel(
            name='CatalogHasChunk',
        ),
        migrations.DeleteModel(
            name='Chunk',
        ),
    ]
