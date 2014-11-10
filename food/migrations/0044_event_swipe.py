# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0043_user_ui_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='swipe',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
