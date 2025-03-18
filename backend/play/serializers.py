"""Django REST Framework serializers for the game models.

This module provides serializers for converting game models to/from JSON:
- PlayerSerializer: Handles player data
- RaceSerializer: Handles race data
- EmpireSerializer: Handles empire data
- GameSerializer: Handles game data
- StartGameSerializer: Handles new game creation requests

These serializers handle data validation, transformation, and API response formatting.
"""

from rest_framework import serializers
from .models import Player, Race, Empire, Game
from celestial.models import System
from .start import GalaxySize


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for Player model.
    
    Handles conversion of Player instances to/from JSON for API responses.
    """
    class Meta:
        model = Player
        fields = ['id', 'player_type']
        read_only_fields = ['id']


class RaceSerializer(serializers.ModelSerializer):
    """Serializer for Race model.
    
    Handles conversion of Race instances to/from JSON for API responses.
    """
    class Meta:
        model = Race
        fields = ['id', 'name']
        read_only_fields = ['id']


class EmpireSerializer(serializers.ModelSerializer):
    """Serializer for Empire model.
    
    Handles conversion of Empire instances to/from JSON for API responses.
    Includes related player and race information.
    """
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(),
        source='player',
        write_only=True,
        help_text="The player controlling this empire"
    )
    race = RaceSerializer(read_only=True)
    race_id = serializers.PrimaryKeyRelatedField(
        queryset=Race.objects.all(),
        source='race',
        write_only=True,
        help_text="The race of this empire"
    )
    resource_capacities = serializers.SerializerMethodField(
        help_text="Total resource storage capacities from all controlled planets"
    )

    class Meta:
        model = Empire
        fields = [
            'id', 'name', 'player', 'player_id', 'race', 'race_id', 'game',
            'planets', 'asteroid_belts', 'mineral_storage', 'organic_storage',
            'radioactive_storage', 'exotic_storage', 'resource_capacities'
        ]
        read_only_fields = ['id']

    def get_resource_capacities(self, obj):
        """Calculate total resource storage capacities.
        
        Args:
            obj (Empire): The empire instance
            
        Returns:
            dict: Total storage capacities for each resource type
        """
        return {
            'mineral_capacity': obj.mineral_capacity,
            'organic_capacity': obj.organic_capacity,
            'radioactive_capacity': obj.radioactive_capacity,
            'exotic_capacity': obj.exotic_capacity
        }


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game model.
    
    Handles conversion of Game instances to/from JSON for API responses.
    Includes related empires and systems information.
    """
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
        """Validate that game meets minimum requirements.
        
        Ensures that:
        - Game has at least 2 empires
        - Game has at least 2 star systems
        
        Note:
            This validation only runs on updates since empires and systems
            are added after game creation.
            
        Args:
            data (dict): The data to validate
            
        Returns:
            dict: The validated data
            
        Raises:
            ValidationError: If minimum requirements are not met
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
    """Serializer for new game creation requests.
    
    Handles validation and conversion of game creation parameters.
    """
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
        """Validate and convert galaxy size value.
        
        Args:
            value (str): The galaxy size value to validate
            
        Returns:
            GalaxySize: The validated galaxy size enum value
            
        Raises:
            ValidationError: If the galaxy size is invalid
        """
        try:
            return GalaxySize(value.lower())
        except ValueError:
            raise serializers.ValidationError('Invalid galaxy size')

    def validate(self, data):
        """Validate all required fields are present.
        
        Args:
            data (dict): The data to validate
            
        Returns:
            dict: The validated data
            
        Raises:
            ValidationError: If any required field is missing
        """
        if not data.get('player_empire_name'):
            raise serializers.ValidationError({'player_empire_name': 'This field is required'})
        if 'computer_empire_count' not in data:
            raise serializers.ValidationError({'computer_empire_count': 'This field is required'})
        if not data.get('galaxy_size'):
            raise serializers.ValidationError({'galaxy_size': 'This field is required'})
        return data
