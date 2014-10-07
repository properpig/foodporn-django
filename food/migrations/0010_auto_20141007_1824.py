# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_auto_20141007_1820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_friend',
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to='food.User'),
            preserve_default=True,
        ),
    ]
