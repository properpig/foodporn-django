# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0008_user_restaurants_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='is_liked',
        ),
        migrations.AddField(
            model_name='user',
            name='foods_liked',
            field=models.ManyToManyField(related_name=b'foods_liked', to='food.Restaurant'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='restaurants_following',
            field=models.ManyToManyField(related_name=b'restaurants_following', to=b'food.Restaurant'),
        ),
    ]
