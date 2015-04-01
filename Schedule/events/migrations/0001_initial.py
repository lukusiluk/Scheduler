# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.IntegerField(max_length=10)),
                ('Hour', models.CharField(max_length=200)),
                ('Day', models.CharField(max_length=200)),
                ('Subject', models.CharField(max_length=200)),
                ('Teachers', models.CharField(max_length=200)),
                ('Students', models.CharField(max_length=200)),
                ('Tag', models.CharField(max_length=200)),
                ('Room', models.CharField(max_length=200)),
                ('Comment', models.CharField(blank=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('wyklad', models.CharField(max_length=10)),
                ('cwiczenia', models.CharField(max_length=10)),
                ('laboratoryjna', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
