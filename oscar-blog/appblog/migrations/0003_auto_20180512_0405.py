# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-12 04:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appblog', '0002_auto_20180512_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractpost',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='abstractpost',
            name='excerpt',
            field=models.TextField(),
        ),
    ]
