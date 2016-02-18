from rest_framework import serializers

from bestiary.models import Monster, Skill, LeaderSkill, Effect, ScalesWith, ScalingStat, Source
from herders.models import Summoner, MonsterInstance, RuneInstance, TeamGroup, Team


# Read-only monster database stuff.
class MonsterSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        exclude = ['meta_order', 'icon_filename']


class MonsterSkillEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = ('name', 'is_buff', 'description', 'icon_filename')


class MonsterSkillScalingStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScalingStat
        fields = ('stat',)


class MonsterSkillScalesWithSerializer(serializers.ModelSerializer):
    stat = serializers.ReadOnlyField(source='scalingstat.stat')

    class Meta:
        model = ScalesWith
        fields = ('stat', 'multiplier')


class MonsterSkillSerializer(serializers.HyperlinkedModelSerializer):
    skill_effect = MonsterSkillEffectSerializer(many=True, read_only=True)
    scales_with = MonsterSkillScalesWithSerializer(source='monsterskillscaleswith_set', many=True, read_only=True)

    class Meta:
        model = Skill
        fields = (
            'pk', 'name', 'description', 'slot', 'cooltime', 'hits', 'passive', 'max_level', 'level_progress_description',
            'skill_effect', 'atk_multiplier', 'scales_with',
            'icon_filename',
        )


class MonsterLeaderSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderSkill


# Small serializer for necessary info for awakens_from/to on main MonsterSerializer
class AwakensMonsterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monster
        fields = ('pk', 'name', 'image_filename')


class MonsterSerializer(serializers.HyperlinkedModelSerializer):
    leader_skill = MonsterLeaderSkillSerializer(read_only=True)
    awakens_from = AwakensMonsterSerializer(read_only=True)
    awakens_to = AwakensMonsterSerializer(read_only=True)
    source = MonsterSourceSerializer(many=True, read_only=True)
    skills = MonsterSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Monster
        fields = (
            'pk', 'name', 'image_filename', 'element', 'archetype', 'base_stars',
            'obtainable', 'can_awaken', 'is_awakened', 'awaken_bonus',
            'skills', 'leader_skill',
            'base_hp', 'base_attack', 'base_defense', 'speed', 'crit_rate', 'crit_damage', 'resistance', 'accuracy',
            'awakens_from', 'awakens_to',
            'awaken_mats_fire_low', 'awaken_mats_fire_mid', 'awaken_mats_fire_high',
            'awaken_mats_water_low', 'awaken_mats_water_mid', 'awaken_mats_water_high',
            'awaken_mats_wind_low', 'awaken_mats_wind_mid', 'awaken_mats_wind_high',
            'awaken_mats_light_low', 'awaken_mats_light_mid', 'awaken_mats_light_high',
            'awaken_mats_dark_low', 'awaken_mats_dark_mid', 'awaken_mats_dark_high',
            'awaken_mats_magic_low', 'awaken_mats_magic_mid', 'awaken_mats_magic_high',
            'source', 'fusion_food'
        )


# Limited fields for displaying list view sort of display.
class MonsterSummarySerializer(serializers.HyperlinkedModelSerializer):
    awakens_from = AwakensMonsterSerializer(read_only=True)
    awakens_to = AwakensMonsterSerializer(read_only=True)

    class Meta:
        model = Monster
        fields = (
            'pk', 'name', 'element', 'archetype', 'base_stars',
            'obtainable', 'can_awaken', 'is_awakened', 'awakens_from', 'awakens_to',
            'fusion_food',
        )


# Individual collection stuff
class SummonerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Summoner
        fields = ('id', 'summoner_name', 'global_server',)


class RuneInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RuneInstance
        fields = (
            'pk', 'type', 'get_type_display', 'owner', 'assigned_to',
            'stars', 'level', 'slot', 'quality', 'value', 'get_quality_display',
            'main_stat', 'get_main_stat_rune_display', 'main_stat_value',
            'innate_stat', 'get_innate_stat_rune_display', 'innate_stat_value',
            'substat_1', 'get_substat_1_rune_display', 'substat_1_value',
            'substat_2', 'get_substat_2_rune_display', 'substat_2_value',
            'substat_3', 'get_substat_3_rune_display', 'substat_3_value',
            'substat_4', 'get_substat_4_rune_display', 'substat_4_value',
            'PERCENT_STATS', 'efficiency',
        )


class TeamGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeamGroup
        fields = [
            'pk', 'name',
        ]


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    group = TeamGroupSerializer()

    class Meta:
        model = Team
        fields = [
            'pk', 'name', 'group'
        ]


class MonsterInstanceSerializer(serializers.HyperlinkedModelSerializer):
    monster = MonsterSerializer(read_only=True)
    team_leader = TeamSerializer(many=True)
    team_set = TeamSerializer(many=True)
    runeinstance_set = RuneInstanceSerializer(many=True)

    class Meta:
        model = MonsterInstance
        fields = (
            'pk', 'monster', 'stars', 'level',
            'skill_1_level', 'skill_2_level', 'skill_3_level', 'skill_4_level',
            'fodder', 'in_storage', 'ignore_for_fusion', 'priority', 'notes',
            'base_hp', 'base_attack', 'base_defense', 'base_speed', 'base_crit_rate', 'base_crit_damage', 'base_resistance', 'base_accuracy',
            'rune_hp', 'rune_attack', 'rune_defense', 'rune_speed', 'rune_crit_rate', 'rune_crit_damage', 'rune_resistance', 'rune_accuracy',
            'hp', 'attack', 'defense', 'speed', 'crit_rate', 'crit_damage', 'resistance', 'accuracy',
            'team_leader', 'team_set',
            'runeinstance_set'
        )
        depth = 1
