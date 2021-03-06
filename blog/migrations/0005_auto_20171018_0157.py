# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 01:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0004_auto_20171017_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.CharField(default='Not Defined', max_length=50),
        ),
        migrations.AddField(
            model_name='blog',
            name='othercontributors',
            field=models.ManyToManyField(related_name='_blog_othercontributors_+', to='blog.BlogAuthor'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.TextField(help_text='Enter you blog text here.'),
        ),
    ]
