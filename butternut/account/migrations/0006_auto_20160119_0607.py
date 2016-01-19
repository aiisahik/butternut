# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20160119_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='elo',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mu',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sigma',
        ),
    ]
