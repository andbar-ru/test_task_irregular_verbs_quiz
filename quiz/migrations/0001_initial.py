# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verb',
            fields=[
                ('base_form', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('past_simple', models.CharField(max_length=30)),
                ('past_participle', models.CharField(max_length=30)),
            ],
        ),
    ]
