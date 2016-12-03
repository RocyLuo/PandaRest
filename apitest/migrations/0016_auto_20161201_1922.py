# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0015_operationlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='dboperation',
            name='skip',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requestoperation',
            name='skip',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operationlog',
            name='assert_result',
            field=models.CharField(choices=[('PASS', 'PASS'), ('FAIL', 'FAIL'), ('ERROR', 'ERROR'), ('SKIP', 'SKIP')], max_length=10),
        ),
    ]
