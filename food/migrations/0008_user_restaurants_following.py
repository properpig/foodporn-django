# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_food_num_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='restaurants_following',
            field=models.ManyToManyField(to='food.Restaurant'),
            preserve_default=True,
        ),
    ]
