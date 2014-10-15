# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0035_auto_20141015_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='is_chinese',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_cholesterolfree',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_french',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_german',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_glutenfree',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_halal',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_indian',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_italian',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_japanese',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_korean',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_lactosefree',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_mexican',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_middleeast',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_organic',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_seafood',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_thai',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_vegan',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_vegetarian',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_vietnamese',
        ),
        migrations.RemoveField(
            model_name='food',
            name='is_western',
        ),
    ]
