# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 17:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField()),
                ('status', models.SmallIntegerField(default=0)),
                ('priority', models.SmallIntegerField(default=1)),
                ('type', models.CharField(choices=[('Project', 'Project'), ('Module', 'Module'), ('Template', 'Template'), ('Case', 'Case')], max_length=50)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('repeat', models.SmallIntegerField(default=1)),
                ('parent', models.ForeignKey(blank=True, default=-1, null=True, on_delete=django.db.models.deletion.CASCADE, to='apitest.Catalog')),
            ],
        ),
        migrations.CreateModel(
            name='DBOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField(default='')),
                ('sql', models.TextField()),
                ('priority', models.SmallIntegerField(default=1)),
                ('skip', models.SmallIntegerField(default=0)),
                ('catalog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apitest.Catalog')),
            ],
        ),
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('module_name', models.CharField(max_length=50)),
                ('case_name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('operation_info', models.TextField()),
                ('operation_result', models.TextField(blank=True, null=True)),
                ('assert_result', models.CharField(choices=[('Pass', 'Pass'), ('Fail', 'Fail'), ('Error', 'Error'), ('Skip', 'Skip')], max_length=6)),
                ('assert_info', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('project_id', models.IntegerField()),
                ('project_name', models.CharField(max_length=50)),
                ('case_total', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('case_pass', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('case_fail', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('case_error', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('case_skip', models.SmallIntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField(default='')),
                ('is_template', models.SmallIntegerField(default=0)),
                ('method', models.CharField(choices=[('get', 'get'), ('post', 'post'), ('put', 'put'), ('delete', 'delete')], max_length=10)),
                ('url', models.URLField(max_length=300)),
                ('header', models.CharField(blank=True, max_length=500, null=True)),
                ('params', models.CharField(blank=True, max_length=300, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('expect_status', models.SmallIntegerField(blank=True, default=200, null=True)),
                ('test_code', models.TextField(blank=True, null=True)),
                ('priority', models.SmallIntegerField(default=1)),
                ('skip_next', models.SmallIntegerField(default=0)),
                ('wait_timeout', models.SmallIntegerField(default=0)),
                ('wait_period', models.SmallIntegerField(default=0)),
                ('drive_data', models.TextField(default='')),
                ('catalog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apitest.Catalog')),
            ],
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=500)),
                ('catalog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apitest.Catalog')),
            ],
        ),
        migrations.AddField(
            model_name='operationlog',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apitest.Report'),
        ),
        migrations.AlterUniqueTogether(
            name='catalog',
            unique_together=set([('name', 'type')]),
        ),
    ]
