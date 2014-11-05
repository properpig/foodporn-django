# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0040_auto_20141104_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='handphone',
            field=models.CharField(max_length=14, null=True),
            preserve_default=True,
        ),
    ]
