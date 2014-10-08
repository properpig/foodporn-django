# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0014_remove_food_num_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='is_following',
            new_name='is_recommended',
        ),
    ]
