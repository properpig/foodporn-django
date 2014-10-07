# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_remove_food_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='restaurant',
            field=models.ForeignKey(blank=True, to='food.Restaurant', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='review',
            name='restaurant',
            field=models.ForeignKey(blank=True, to='food.Restaurant', null=True),
        ),
    ]
