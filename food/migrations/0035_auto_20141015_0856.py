# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0034_auto_20141015_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='cuisine',
            field=models.ManyToManyField(to='food.Cuisine', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='food',
            name='dietary',
            field=models.ManyToManyField(to='food.Diet', null=True, blank=True),
            preserve_default=True,
        ),
    ]
