from rest_framework import serializers
from .models import Planet


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
        ] 