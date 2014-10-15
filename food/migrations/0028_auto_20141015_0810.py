# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0027_auto_20141015_0804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='is_malaysian',
            new_name='is_thai',
        ),
    ]
