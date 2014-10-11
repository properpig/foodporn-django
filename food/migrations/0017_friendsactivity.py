# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0016_dealsactivity'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendsActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(related_name=b'actor', blank=True, to='food.User', null=True)),
                ('friend', models.ForeignKey(related_name=b'friend', blank=True, to='food.User', null=True)),
                ('restaurant', models.ForeignKey(blank=True, to='food.Restaurant', null=True)),
                ('review', models.ForeignKey(blank=True, to='food.Review', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
