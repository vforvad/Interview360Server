# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 20:46
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0005_auto_20180123_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=255, unique=True)),
                ('phone_comment', models.TextField()),
                ('social_networks', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='resumes.Resume')),
            ],
            options={
                'db_table': 'contacts',
            },
        ),
    ]