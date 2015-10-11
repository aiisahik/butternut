# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_auto_20151006_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='loser_position',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'EAST', b'EAST'), (b'WEST', b'WEST')]),
        ),
        migrations.AddField(
            model_name='match',
            name='winner_position',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'EAST', b'EAST'), (b'WEST', b'WEST')]),
        ),
    ]
