# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_auto_20141007_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='price',
            new_name='price_high',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='price_low',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]
