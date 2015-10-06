# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151006_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mu',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='sigma',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
