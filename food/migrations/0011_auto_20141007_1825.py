# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20141007_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='foods_liked',
            field=models.ManyToManyField(related_name=b'foods_liked', to=b'food.Food'),
        ),
    ]
