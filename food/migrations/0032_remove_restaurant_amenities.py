# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0031_auto_20141015_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='amenities',
        ),
    ]
