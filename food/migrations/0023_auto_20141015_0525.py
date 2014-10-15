# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0022_auto_20141014_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default=b'Eating since 1988!', max_length=400),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='location_x',
            field=models.CharField(default=b'1.296568', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='location_y',
            field=models.CharField(default=b'103.852118', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name=b'followers', null=True, to=b'food.User', blank=True),
        ),
    ]
