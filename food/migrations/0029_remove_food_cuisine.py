# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0028_auto_20141015_0810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='cuisine',
        ),
    ]
