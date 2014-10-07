# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20141007_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='email',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='opening_hours',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='postal_code',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='telephone',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
