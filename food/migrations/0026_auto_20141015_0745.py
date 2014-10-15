# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0025_auto_20141015_0545'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='is_fatfree',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='food',
            name='is_fruitarian',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='food',
            name='is_glutenfree',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='food',
            name='is_lactosefree',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='food',
            name='is_vegetarian',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
