# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-23 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20191123_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='school',
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='enrolled_date',
            field=models.DateField(auto_now_add=True, verbose_name='报名日期'),
        ),
    ]