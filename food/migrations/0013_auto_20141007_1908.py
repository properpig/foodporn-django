# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0012_auto_20141007_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='foods_liked',
            field=models.ManyToManyField(related_name=b'foods_liked', null=True, to=b'food.Food', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', null=True, to=b'food.User', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='restaurants_following',
            field=models.ManyToManyField(related_name=b'restaurants_following', null=True, to=b'food.Restaurant', blank=True),
        ),
    ]
