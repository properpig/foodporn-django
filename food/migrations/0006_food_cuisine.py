# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20141007_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='cuisine',
            field=models.CharField(default='none', max_length=30),
            preserve_default=False,
        ),
    ]
