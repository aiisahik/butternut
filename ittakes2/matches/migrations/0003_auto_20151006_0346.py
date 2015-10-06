# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_auto_20151006_0345'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='loser_mu',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='match',
            name='loser_sigma',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
