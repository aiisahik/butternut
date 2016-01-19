# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151006_0207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('winner_score', models.SmallIntegerField(null=True, blank=True)),
                ('loser_score', models.SmallIntegerField(null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('expire_date', models.DateTimeField(null=True, blank=True)),
                ('loser', models.ForeignKey(related_query_name=b'loser', related_name='losers', to='account.Profile')),
                ('winner', models.ForeignKey(related_query_name=b'winner', related_name='winners', to='account.Profile')),
            ],
        ),
    ]
