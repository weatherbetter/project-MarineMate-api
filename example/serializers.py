from rest_framework import serializers

from .models import LifesavingEquipment


class CalcSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifesavingEquipment
        fields = ("equipment_long", "equipment_lat", "spot")
