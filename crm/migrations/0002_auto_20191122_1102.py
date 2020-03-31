# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-22 03:02
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='course',
            field=models.CharField(choices=[('Linux', 'Linux运维'), ('Python', 'Python全栈')], max_length=64, verbose_name='课程名称'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='class_list',
            field=models.ManyToManyField(blank=True, to='crm.ClassList', verbose_name='已报班级'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='course',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Linux', 'Linux运维'), ('Python', 'Python全栈')], max_length=12, verbose_name='咨询课程'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sex',
            field=models.CharField(blank=True, choices=[('男', '男'), ('女', '女')], default='male', max_length=16, null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='course',
            field=models.CharField(blank=True, choices=[('Linux', 'Linux运维'), ('Python', 'Python全栈')], default='Linux', max_length=64, null=True, verbose_name='课程名'),
        ),
    ]