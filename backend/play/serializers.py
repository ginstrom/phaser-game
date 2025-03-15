from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'player_type']
        read_only_fields = ['id']
