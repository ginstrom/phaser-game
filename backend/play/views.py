"""Django REST Framework views for the game API.

This module provides ViewSets for managing game entities through the REST API:
- PlayerViewSet: Manages player instances
- RaceViewSet: Manages race instances
- EmpireViewSet: Manages empire instances and related resources
- GameViewSet: Manages game instances and game-specific actions

These views handle HTTP requests and coordinate with models and serializers
to provide the game's API endpoints.
"""

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
from celestial.serializers import SystemSerializer, PlanetSerializer, AsteroidBeltSerializer
from .start import start_game, GalaxySize
from .turn import process

# Create your views here.

@extend_schema(tags=['players'])
class PlayerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing player instances.
    
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
    """ViewSet for managing race instances.
    
    Provides CRUD operations for races in the game:
    * List all races
    * Create a new race
    * Retrieve a specific race
    * Update race details
    * Delete a race
    """
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


@extend_schema(tags=['empires'])
class EmpireViewSet(viewsets.ModelViewSet):
    """ViewSet for managing empire instances.
    
    Provides CRUD operations for empires in the game:
    * List all empires
    * Create a new empire
    * Retrieve a specific empire
    * Update empire details
    * Delete an empire
    
    Additional endpoints:
    * GET /api/empires/{id}/planets/ - List all planets belonging to the empire
    * GET /api/empires/{id}/asteroid-belts/ - List all asteroid belts belonging to the empire
    """
    queryset = Empire.objects.all()
    serializer_class = EmpireSerializer

    @extend_schema(
        description='Get all planets belonging to this empire',
        responses={200: PlanetSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def planets(self, request, pk=None):
        """Get all planets belonging to this empire.
        
        Args:
            request: The HTTP request
            pk: The empire ID
            
        Returns:
            Response: List of planets belonging to the empire
        """
        empire = self.get_object()
        planets = empire.planets
        serializer = PlanetSerializer(planets, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='Get all asteroid belts belonging to this empire',
        responses={200: AsteroidBeltSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_path='asteroid-belts')
    def asteroid_belts(self, request, pk=None):
        """Get all asteroid belts belonging to this empire.
        
        Args:
            request: The HTTP request
            pk: The empire ID
            
        Returns:
            Response: List of asteroid belts belonging to the empire
        """
        empire = self.get_object()
        asteroid_belts = empire.asteroid_belts
        serializer = AsteroidBeltSerializer(asteroid_belts, many=True)
        return Response(serializer.data)


@extend_schema(tags=['games'])
class GameViewSet(viewsets.ModelViewSet):
    """ViewSet for managing game instances.
    
    Provides endpoints for creating, retrieving, updating and deleting games,
    as well as game-specific actions like ending turns and starting new games.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        """Create a new game starting at turn 0.
        
        Args:
            serializer: The serializer instance containing the game data
        """
        serializer.save(turn=0)

    @extend_schema(
        description='Get all systems in this game',
        responses={200: SystemSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def systems(self, request, pk=None):
        """Get all systems in this game.
        
        Args:
            request: The HTTP request
            pk: The game ID
            
        Returns:
            Response: List of systems in the game
        """
        game = self.get_object()
        systems = game.systems.all()
        serializer = SystemSerializer(systems, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='Get all empires in this game',
        responses={200: EmpireSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def empires(self, request, pk=None):
        """Get all empires in this game.
        
        Args:
            request: The HTTP request
            pk: The game ID
            
        Returns:
            Response: List of empires in the game
        """
        game = self.get_object()
        empires = game.empires.all()
        serializer = EmpireSerializer(empires, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='End the current turn and start the next one',
        request=None,
        responses={200: GameSerializer}
    )
    @action(detail=True, methods=['post'], url_path='end-turn')
    def end_turn(self, request, pk=None):
        """End the current turn and start the next one.
        
        This action:
        1. Retrieves the current game
        2. Processes the end of turn
        3. Returns the updated game state
        
        Args:
            request: The HTTP request
            pk: The primary key of the game
            
        Returns:
            Response: The updated game data
        """
        game = self.get_object()
        game = process(game)
        
        serializer = self.get_serializer(game)
        return Response(serializer.data)

    @extend_schema(
        description='Start a new game with the specified parameters',
        request=StartGameSerializer,
        responses={
            201: {
                'type': 'object',
                'description': 'Game successfully created',
                '$ref': '#/components/schemas/Game'
            },
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
        """Start a new game with the specified parameters.
        
        This action:
        1. Validates the game creation parameters
        2. Creates a new game with the specified configuration
        3. Returns the created game
        
        Args:
            request: The HTTP request containing game parameters
            
        Returns:
            Response: The created game data or error message
            
        Raises:
            ValidationError: If the game parameters are invalid
        """
        serializer = StartGameSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
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
