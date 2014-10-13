# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0018_user_is_recommended'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='foods_disliked',
            field=models.ManyToManyField(related_name=b'foods_disliked', null=True, to='food.Food', blank=True),
            preserve_default=True,
        ),
    ]
