# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_food_cuisine'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='num_likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
