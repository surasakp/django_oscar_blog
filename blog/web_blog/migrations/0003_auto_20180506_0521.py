# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-06 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_blog', '0002_auto_20180506_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractpost',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/%Y/%m/', verbose_name='Featured Image'),
        ),
    ]