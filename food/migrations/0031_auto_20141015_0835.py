# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0030_auto_20141015_0829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_bar',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_kidsarea',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_open24',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_petfriendly',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_smokingarea',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_television',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_valetparking',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='has_wifi',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='amenities',
            field=models.ForeignKey(blank=True, to='food.Amenity', null=True),
            preserve_default=True,
        ),
    ]
