# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-12 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appblog', '0004_auto_20180512_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractpost',
            name='excerpt',
            field=models.TextField(),
        ),
    ]
