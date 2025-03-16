from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Player, Race, Empire, Game
from .serializers import (
    PlayerSerializer, 
    RaceSerializer, 
    EmpireSerializer, 
    GameSerializer,
    StartGameSerializer
)
from .start import start_game, GalaxySize

# Create your views here.

@extend_schema(tags=['players'])
class PlayerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing player instances.
    
    Provides CRUD operations for players in the game:
    * List all players
    * Create a new player
    * Retrieve a specific player
    * Update player details
    * Delete a player
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


@extend_schema(tags=['races'])
class RaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing alien races.
    
    Provides CRUD operations for different alien races in the game:
    * List all available races
    * Create a new race
    * Retrieve race details
    * Update race characteristics
    * Delete a race
    
    Each race has unique traits and characteristics that affect gameplay.
    """
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


@extend_schema(tags=['empires'])
class EmpireViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing empires in the game.
    
    Provides CRUD operations for empires:
    * List all empires
    * Create a new empire
    * Retrieve empire details
    * Update empire status
    * Delete an empire
    
    Empires are the main actors in the game, representing both player-controlled
    and AI-controlled factions. Each empire belongs to a specific race and has
    its own resources, territory, and technological advancement level.
    """
    queryset = Empire.objects.all()
    serializer_class = EmpireSerializer


@extend_schema(tags=['games'])
class GameViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing game instances.
    
    Provides endpoints for creating, retrieving, updating and deleting games,
    as well as game-specific actions like ending turns and starting new games.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        """Create a new game starting at turn 1"""
        serializer.save(turn=1)

    @extend_schema(
        description='End the current turn and start the next one',
        responses={200: {'properties': {'status': {'type': 'string'}, 'new_turn': {'type': 'integer'}}}}
    )
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

    @extend_schema(
        description='Start a new game with the specified parameters',
        request=StartGameSerializer,
        responses={
            201: GameSerializer,
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'description': 'Error message when request validation fails'}
                }
            }
        }
    )
    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a new game with the specified parameters"""
        serializer = StartGameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid data provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game = start_game(serializer.validated_data)
            response_serializer = self.get_serializer(game)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
