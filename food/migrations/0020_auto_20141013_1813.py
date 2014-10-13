# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0019_user_foods_disliked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_pic',
            new_name='photo',
        ),
    ]
