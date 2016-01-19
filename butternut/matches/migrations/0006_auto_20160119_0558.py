# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20160119_0558'),
        ('matches', '0005_auto_20151011_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mu', models.FloatField(null=True, blank=True)),
                ('sigma', models.FloatField(null=True, blank=True)),
                ('elo', models.FloatField(null=True, blank=True)),
                ('update_date', models.DateTimeField()),
                ('rank', models.SmallIntegerField(null=True, blank=True)),
                ('judge', models.ForeignKey(related_query_name=b'player_judge', related_name='player_judges', to='account.Profile')),
                ('target', models.ForeignKey(related_query_name=b'target', related_name='target', to='account.Profile')),
            ],
        ),
        migrations.RemoveField(
            model_name='match',
            name='loser_elo',
        ),
        migrations.RemoveField(
            model_name='match',
            name='loser_mu',
        ),
        migrations.RemoveField(
            model_name='match',
            name='loser_position',
        ),
        migrations.RemoveField(
            model_name='match',
            name='loser_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='loser_sigma',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner_elo',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner_mu',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner_position',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner_sigma',
        ),
        migrations.AddField(
            model_name='match',
            name='judge',
            field=models.ForeignKey(related_query_name=b'judge', related_name='judges', blank=True, to='account.Profile', null=True),
        ),
    ]
