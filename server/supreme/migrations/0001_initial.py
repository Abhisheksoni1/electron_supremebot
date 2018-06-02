# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('card_number', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('expiry', models.IntegerField()),
                ('year', models.IntegerField()),
                ('address1', models.CharField(max_length=32)),
                ('address2', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32)),
                ('zip_code', models.CharField(max_length=32)),
                ('payment_option', models.CharField(max_length=32)),
                ('country', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('status', models.CharField(max_length=10, default='success', choices=[('success', 'success'), ('error', 'error')])),
                ('speed', models.CharField(max_length=10, default=80)),
                ('action', models.CharField(max_length=10, default='0', choices=[('1', 'Start'), ('0', 'STOP'), ('-1', 'PAUSE')])),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('key', models.CharField(max_length=128)),
                ('moniter', models.IntegerField(default=0)),
                ('checkout_delay', models.IntegerField(default=0)),
                ('gmail', models.CharField(max_length=32, blank=True, default='')),
                ('mode', models.CharField(max_length=10, default='headless', choices=[('headless', 'HEADLESS'), ('normal', 'NORMAL')])),
            ],
        ),
        migrations.CreateModel(
            name='SupremeTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('size', models.CharField(max_length=32)),
                ('color', models.CharField(max_length=16)),
                ('product', models.CharField(max_length=16, default=' ')),
                ('progress', models.CharField(max_length=16, default='Initialise!')),
                ('action', models.CharField(max_length=4, default='0', choices=[('1', 'Start'), ('0', 'STOP'), ('-1', 'PAUSE')])),
                ('keyword', models.CharField(max_length=32)),
                ('category', models.CharField(max_length=32)),
                ('timer', models.IntegerField()),
                ('proxy', models.CharField(max_length=32)),
                ('profile', models.ForeignKey(to='supreme.Profile')),
            ],
        ),
    ]
