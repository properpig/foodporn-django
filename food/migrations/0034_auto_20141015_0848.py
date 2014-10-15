# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0033_restaurant_amenities'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenity',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuisine',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diet',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
