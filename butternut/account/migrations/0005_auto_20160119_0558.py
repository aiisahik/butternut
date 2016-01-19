# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_elo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(default=b'F', max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender_preference',
            field=models.CharField(default=b'M', max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
    ]
