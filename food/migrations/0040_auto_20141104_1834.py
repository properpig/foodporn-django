# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0039_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='page',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
