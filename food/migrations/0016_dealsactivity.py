# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0015_auto_20141008_0152'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealsActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('photo', models.CharField(max_length=200)),
                ('details', models.CharField(max_length=300)),
                ('more_details', models.CharField(max_length=500)),
                ('restaurant', models.ForeignKey(blank=True, to='food.Restaurant', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
