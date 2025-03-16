from rest_framework import serializers
from .models import Player, Race, Empire, Game
from celestial.models import System
from .start import GalaxySize


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


class GameSerializer(serializers.ModelSerializer):
    empires = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text="The empires participating in this game"
    )
    systems = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text="The star systems in this game"
    )

    class Meta:
        model = Game
        fields = ['id', 'turn', 'empires', 'systems']
        read_only_fields = ['id']

    def validate(self, data):
        """
        Validate that game has minimum required empires and systems.
        Note: This validation only runs on updates since empires and systems
        are added after game creation.
        """
        if self.instance:  # Only validate on update
            # Get the instance with current data
            instance = self.instance
            
            # Validate minimum number of empires
            if instance.empires.count() < 2:
                raise serializers.ValidationError('Game must have at least 2 empires.')
            
            # Validate minimum number of systems
            if instance.systems.count() < 2:
                raise serializers.ValidationError('Game must have at least 2 star systems.')
        
        return data


class StartGameSerializer(serializers.Serializer):
    player_empire_name = serializers.CharField(
        help_text="Name of the player's empire",
        required=True
    )
    computer_empire_count = serializers.IntegerField(
        help_text="Number of AI opponents",
        required=True
    )
    galaxy_size = serializers.ChoiceField(
        choices=GalaxySize.choices(),
        help_text="Size of the galaxy (tiny, small, medium, large)",
        required=True
    )

    def validate_galaxy_size(self, value):
        try:
            return GalaxySize(value.lower())
        except ValueError:
            raise serializers.ValidationError('Invalid galaxy size')

    def validate(self, data):
        if not data.get('player_empire_name'):
            raise serializers.ValidationError({'player_empire_name': 'This field is required'})
        if 'computer_empire_count' not in data:
            raise serializers.ValidationError({'computer_empire_count': 'This field is required'})
        if not data.get('galaxy_size'):
            raise serializers.ValidationError({'galaxy_size': 'This field is required'})
        return data
