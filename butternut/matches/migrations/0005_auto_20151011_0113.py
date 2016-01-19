# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0004_auto_20151006_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='loser_elo',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_elo',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
