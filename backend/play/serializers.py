from rest_framework import serializers
from .models import Player, Race, Empire


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'player_type']
        read_only_fields = ['id']


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'name']
        read_only_fields = ['id']


class EmpireSerializer(serializers.ModelSerializer):
    resource_capacities = serializers.SerializerMethodField()

    class Meta:
        model = Empire
        fields = [
            'id', 'name', 'player', 'race', 'planets', 'asteroid_belts',
            'mineral_storage', 'organic_storage', 'radioactive_storage', 'exotic_storage',
            'resource_capacities'
        ]
        read_only_fields = ['id']

    def get_resource_capacities(self, obj):
        """Return all resource capacities in a single dictionary"""
        return {
            'mineral_capacity': obj.mineral_capacity,
            'organic_capacity': obj.organic_capacity,
            'radioactive_capacity': obj.radioactive_capacity,
            'exotic_capacity': obj.exotic_capacity
        }
