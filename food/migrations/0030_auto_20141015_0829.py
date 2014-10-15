# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0029_remove_food_cuisine'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='has_bar',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='has_kidsarea',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='has_open24',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='has_petfriendly',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='has_smokingarea',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='has_television',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='has_valetparking',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='has_wifi',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
