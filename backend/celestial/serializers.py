from rest_framework import serializers
from .models import Planet, Star, AsteroidBelt, System


class PlanetSerializer(serializers.ModelSerializer):
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

class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ['id', 'star_type']

class AsteroidBeltSerializer(serializers.ModelSerializer):
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

class SystemSerializer(serializers.ModelSerializer):
    star = StarSerializer()
    planets = PlanetSerializer(many=True, read_only=True)
    asteroid_belts = AsteroidBeltSerializer(many=True, read_only=True)

    class Meta:
        model = System
        fields = ['id', 'x', 'y', 'star', 'planets', 'asteroid_belts']

    def create(self, validated_data):
        star_data = validated_data.pop('star')
        star = Star.objects.create(**star_data)
        system = System.objects.create(star=star, **validated_data)
        return system

    def update(self, instance, validated_data):
        if 'star' in validated_data:
            star_data = validated_data.pop('star')
            star = instance.star
            for attr, value in star_data.items():
                setattr(star, attr, value)
            star.save()
        return super().update(instance, validated_data) 