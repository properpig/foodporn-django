# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0017_friendsactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_recommended',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
