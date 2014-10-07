# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0013_auto_20141007_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='num_likes',
        ),
    ]
