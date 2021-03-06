from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify


class Dungeon(models.Model):
    CATEGORY_SCENARIO = 0
    CATEGORY_RUNE_DUNGEON = 1
    CATEGORY_ESSENCE_DUNGEON = 2
    CATEGORY_OTHER_DUNGEON = 3
    CATEGORY_RAID = 4
    CATEGORY_HALL_OF_HEROES = 5

    CATEGORY_CHOICES = [
        (CATEGORY_SCENARIO, 'Scenarios'),
        (CATEGORY_RUNE_DUNGEON, 'Rune Dungeons'),
        (CATEGORY_ESSENCE_DUNGEON, 'Elemental Dungeons'),
        (CATEGORY_OTHER_DUNGEON, 'Other Dungeons'),
        (CATEGORY_RAID, 'Raids'),
        (CATEGORY_HALL_OF_HEROES, 'Hall of Heroes'),
    ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    max_floors = models.IntegerField(default=10)
    slug = models.SlugField(blank=True, null=True)
    category = models.IntegerField(choices=CATEGORY_CHOICES, blank=True, null=True)

    # TODO: Remove following fields when Level model is fully utilized everywhere: energy_cost, xp, monster_slots
    # For the following fields:
    # Outer array index is difficulty (normal, hard, hell). Inner array index is the stage/floor
    # Example: Hell B2 is dungeon.energy_cost[RunLog.DIFFICULTY_HELL][1]
    energy_cost = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)), blank=True, null=True)
    xp = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)), blank=True, null=True)
    monster_slots = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)), blank=True, null=True)

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Dungeon, self).save(*args, **kwargs)


class Level(models.Model):
    DIFFICULTY_NORMAL = 1
    DIFFICULTY_HARD = 2
    DIFFICULTY_HELL = 3
    DIFFICULTY_CHOICES = (
        (DIFFICULTY_NORMAL, 'Normal'),
        (DIFFICULTY_HARD, 'Hard'),
        (DIFFICULTY_HELL, 'Hell'),
    )

    dungeon = models.ForeignKey(Dungeon, on_delete=models.CASCADE)
    floor = models.IntegerField()
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, blank=True, null=True)
    energy_cost = models.IntegerField(blank=True, null=True, help_text='Energy cost to start a run')
    xp = models.IntegerField(blank=True, null=True, help_text='XP gained by fully clearing the level')
    frontline_slots = models.IntegerField(
        default=5,
        help_text='Serves as general slots if dungeon does not have front/back lines'
    )
    backline_slots = models.IntegerField(blank=True, null=True, help_text='Leave null for normal dungeons')
    max_slots = models.IntegerField(
        blank=True,
        null=True,
        help_text='Maximum monsters combined front/backline. Not required if backline not specified.'
    )

    class Meta:
        ordering = ('difficulty', 'floor')
        unique_together = ('dungeon', 'floor', 'difficulty')

    def __str__(self):
        return f'{self.dungeon_id} {self.floor} - {self.get_difficulty_display()}'


class GuideBase(models.Model):
    short_text = models.TextField(blank=True, default='')
    long_text = models.TextField(blank=True, default='')
    last_updated = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, editable=False)

    class Meta:
        abstract = True


class MonsterGuide(GuideBase):
    monster = models.OneToOneField('herders.Monster', on_delete=models.CASCADE)

    def __str__(self):
        return f'Monster Guide - {self.monster}'

    class Meta:
        ordering = ['monster__name']
