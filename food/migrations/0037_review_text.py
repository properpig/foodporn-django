# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0036_auto_20141015_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='text',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
    ]
