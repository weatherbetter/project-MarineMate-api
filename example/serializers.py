from rest_framework import serializers

from .models import (
    Beach,
    BeachInfra,
    BeachScore,
    JellyfishScore,
    LifesavingEquipment,
    MaxTemperature,
    RainfallScore,
    WaveHeight,
    WindDirection,
    WindSpeed,
)


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifesavingEquipment
        fields = ("equipment_long", "equipment_lat", "spot")


class BeachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beach
        fields = ("id", "beach_name", "location", "sigungu")


class BeachInfraSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachInfra
        fields = ("shower_room", "toilet", "dressing_room", "watch_tower", "tap_water", "beach_id")


class WindSpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindSpeed
        fields = ["date", "wind_speed"]


class MaxTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaxTemperature
        fields = ["date", "day_max_temp"]


class WaveHeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaveHeight
        fields = ["date", "wave_height"]


class WindDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindDirection
        fields = ["date", "wind_direction"]


class BeachScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachScore
        fields = "__all__"


class JellyfishScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JellyfishScore
        fields = "__all__"


class RainfallScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RainfallScore
        fields = "__all__"
