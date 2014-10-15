# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0032_remove_restaurant_amenities'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='amenities',
            field=models.ManyToManyField(related_name=b'amenities', null=True, to='food.Amenity', blank=True),
            preserve_default=True,
        ),
    ]
