from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Player, Race, Empire, Game
from .serializers import PlayerSerializer, RaceSerializer, EmpireSerializer, GameSerializer

# Create your views here.

class PlayerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Player instances.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class RaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Race instances.
    """
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


class EmpireViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Empire instances.
    """
    queryset = Empire.objects.all()
    serializer_class = EmpireSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing games.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        """Create a new game starting at turn 1"""
        serializer.save(turn=1)

    @action(detail=True, methods=['post'])
    def end_turn(self, request, pk=None):
        """End the current turn and start the next one"""
        game = self.get_object()
        game.turn += 1
        game.save()
        
        # Run any end-of-turn processing here
        
        return Response({
            'status': 'turn ended',
            'new_turn': game.turn
        })
