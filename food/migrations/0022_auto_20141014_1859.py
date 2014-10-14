# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0021_auto_20141013_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name=b'users_following', null=True, to=b'food.User', blank=True),
        ),
    ]
