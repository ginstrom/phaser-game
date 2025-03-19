"""Serializers for celestial bodies in the game API.

This module provides serializers for converting celestial models to/from JSON:

**Serializers:**
- :serializer:`celestial.PlanetSerializer`: Handles planet resource fields
- :serializer:`celestial.StarSerializer`: Handles star type selection
- :serializer:`celestial.AsteroidBeltSerializer`: Handles asteroid belt resources
- :serializer:`celestial.SystemSerializer`: Handles nested celestial objects
"""

from rest_framework import serializers
from .models import Planet, Star, AsteroidBelt, System
from play.models import Game


class PlanetSerializer(serializers.ModelSerializer):
    """Serializer for Planet model.
    
    **Fields:**
    - Resource production rates (decimal, 2 places)
    - Storage capacities (decimal, 2 places)
    - Orbital position
    
    **Validation:**
    - All decimal fields use 2 decimal places
    - Maximum 10 digits for decimal fields
    """
    mineral_production = serializers.DecimalField(max_digits=10, decimal_places=2)
    organic_production = serializers.DecimalField(max_digits=10, decimal_places=2)
    radioactive_production = serializers.DecimalField(max_digits=10, decimal_places=2)
    exotic_production = serializers.DecimalField(max_digits=10, decimal_places=2)
    mineral_storage_capacity = serializers.DecimalField(max_digits=10, decimal_places=2)
    organic_storage_capacity = serializers.DecimalField(max_digits=10, decimal_places=2)
    radioactive_storage_capacity = serializers.DecimalField(max_digits=10, decimal_places=2)
    exotic_storage_capacity = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Planet
        fields = [
            'id',
            'mineral_production',
            'organic_production',
            'radioactive_production',
            'exotic_production',
            'mineral_storage_capacity',
            'organic_storage_capacity',
            'radioactive_storage_capacity',
            'exotic_storage_capacity',
            'orbit',
        ]
        read_only_fields = ['id']


class AsteroidBeltSerializer(serializers.ModelSerializer):
    """Serializer for AsteroidBelt model.
    
    **Fields:**
    - Resource production rates (decimal, 2 places)
    - Orbital position
    
    **Validation:**
    - All decimal fields use 2 decimal places
    - Maximum 10 digits for decimal fields
    """
    mineral_production = serializers.DecimalField(max_digits=10, decimal_places=2)
    organic_production = serializers.DecimalField(max_digits=10, decimal_places=2)
    radioactive_production = serializers.DecimalField(max_digits=10, decimal_places=2)
    exotic_production = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = AsteroidBelt
        fields = [
            'id',
            'mineral_production',
            'organic_production',
            'radioactive_production',
            'exotic_production',
            'orbit',
        ]
        read_only_fields = ['id']


class StarSerializer(serializers.ModelSerializer):
    """Serializer for Star model.
    
    **Fields:**
    - Star type (enum)
    """
    class Meta:
        model = Star
        fields = ['id', 'star_type']
        read_only_fields = ['id']


class SystemSerializer(serializers.ModelSerializer):
    """Serializer for System model.
    
    **Fields:**
    - Coordinates (x, y)
    - Star information
    - Planets and asteroid belts
    """
    star = StarSerializer()
    planets = PlanetSerializer(many=True, read_only=True)
    asteroid_belts = AsteroidBeltSerializer(many=True, read_only=True)

    class Meta:
        model = System
        fields = ['id', 'x', 'y', 'star', 'planets', 'asteroid_belts']
        read_only_fields = ['id']

    def validate(self, data):
        """Ensure system coordinates are unique within a game.
        
        **Validation:**
        - Check for existing system at same coordinates
        - Consider game context (null or specific game)
        - Exclude current instance when updating
        """
        x = data.get('x')
        y = data.get('y')
        game = data.get('game')

        # Check if a system with these coordinates already exists in this game
        existing = System.objects.filter(x=x, y=y)
        if game is not None:
            existing = existing.filter(game=game)
        else:
            existing = existing.filter(game__isnull=True)

        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise serializers.ValidationError(
                {'coordinates': 'A system with these coordinates already exists in this game.'}
            )
        return data

    def create(self, validated_data):
        """Create a system with its star.
        
        **Process:**
        1. Extract star data
        2. Create star
        3. Create system with star
        """
        star_data = validated_data.pop('star')
        star = Star.objects.create(**star_data)
        system = System.objects.create(star=star, **validated_data)
        return system

    def update(self, instance, validated_data):
        """Update a system and its star.
        
        **Process:**
        1. Update star if star data provided
        2. Update system fields
        """
        if 'star' in validated_data:
            star_data = validated_data.pop('star')
            star = instance.star
            for attr, value in star_data.items():
                setattr(star, attr, value)
            star.save()
        return super().update(instance, validated_data) 