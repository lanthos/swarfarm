# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-06 05:31
from __future__ import unicode_literals

from django.db import migrations


def create_levels(apps, schema_editor):
    Dungeon = apps.get_model('bestiary', 'Dungeon')
    Level = apps.get_model('bestiary', 'Level')

    for d in Dungeon.objects.all():
        is_scenario = len(d.energy_cost) == 3

        for difficulty in range(len(d.energy_cost)):
            for stage in range(len(d.energy_cost[difficulty])):
                l = Level()
                l.dungeon = d
                l.floor = stage + 1

                if is_scenario:
                    l.difficulty = difficulty + 1

                try:
                    l.energy_cost = d.energy_cost[difficulty][stage]
                except IndexError:
                    # Dungeon has energy_cost defined but not for this combo of difficulty/stage
                    print(f'Energy cost missing for {d} difficulty {difficulty} stage {stage}')
                except TypeError:
                    # Dungeon does not have energy_cost defined at all
                    print(f'Energy cost not defined for {d} difficulty {difficulty} stage {stage}. Add via admin later.')

                try:
                    l.xp = d.xp[difficulty][stage]
                except IndexError:
                    # Dungeon has xp defined but not for this combo of difficulty/stage
                    print(f'XP missing for {d} difficulty {difficulty} stage {stage}')
                except TypeError:
                    # Dungeon does not have xp defined at all
                    print(f'XP not defined for {d} difficulty {difficulty} stage {stage}. Add via admin later.')

                try:
                    l.frontline_slots = d.monster_slots[difficulty][stage]
                except IndexError:
                    # Dungeon has monster_slots defined but not for this combo of difficulty/stage
                    print(f'Monster slots missing for {d} difficulty {difficulty} stage {stage}')
                except TypeError:
                    # Dungeon does not have monster_slots defined at all
                    print(f'Monster slots not defined for {d} difficulty {difficulty} stage {stage}. Add via admin later.')

                l.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('bestiary', '0005_auto_20181105_2129'),
    ]

    operations = [
        migrations.RunPython(create_levels, do_nothing),
    ]
