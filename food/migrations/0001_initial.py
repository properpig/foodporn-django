# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('photo', models.CharField(max_length=200)),
                ('is_halal', models.BooleanField(default=False)),
                ('is_vegan', models.BooleanField(default=False)),
                ('is_liked', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('photo', models.CharField(max_length=200)),
                ('location_name', models.CharField(max_length=200)),
                ('location_x', models.CharField(max_length=20)),
                ('location_y', models.CharField(max_length=20)),
                ('is_following', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.CharField(max_length=200)),
                ('rating', models.IntegerField()),
                ('restaurant', models.ForeignKey(to='food.Restaurant', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('profile_pic', models.CharField(max_length=200)),
                ('is_friend', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(to='food.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='food',
            name='restaurant',
            field=models.ForeignKey(to='food.Restaurant', null=True),
            preserve_default=True,
        ),
    ]
