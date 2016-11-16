# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, auto_created=True, to=settings.AUTH_USER_MODEL, parent_link=True, serialize=False)),
                ('dni', models.IntegerField(null=True, blank=True)),
                ('sex', models.IntegerField(verbose_name='sexo', choices=[(0, 'masculino'), (1, 'femenino')], default=0)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
