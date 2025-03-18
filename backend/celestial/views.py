"""API endpoints for managing celestial bodies in the game.

This module provides REST API endpoints for managing celestial objects:

**ViewSets:**
- :view:`celestial.PlanetViewSet`: CRUD operations for planets
- :view:`celestial.StarViewSet`: CRUD operations for stars
- :view:`celestial.AsteroidBeltViewSet`: CRUD operations for asteroid belts
- :view:`celestial.SystemViewSet`: CRUD operations for star systems
"""

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Planet, Star, AsteroidBelt, System
from .serializers import (
    PlanetSerializer, 
    StarSerializer, 
    AsteroidBeltSerializer,
    SystemSerializer
)

# Create your views here.

class PlanetViewSet(viewsets.ModelViewSet):
    """Manage planets through the API.
    
    **Operations:**
    - List all planets
    - Create new planet
    - Retrieve planet details
    - Update planet
    - Delete planet
    
    **Fields:**
    - Resource production rates
    - Storage capacities
    - Orbital position
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

class StarViewSet(viewsets.ModelViewSet):
    """Manage stars through the API.
    
    **Operations:**
    - List all stars
    - Create new star
    - Retrieve star details
    - Update star
    - Delete star
    
    **Fields:**
    - Star type (blue, white, yellow, orange, brown)
    """
    queryset = Star.objects.all()
    serializer_class = StarSerializer

class AsteroidBeltViewSet(viewsets.ModelViewSet):
    """Manage asteroid belts through the API.
    
    **Operations:**
    - List all asteroid belts
    - Create new asteroid belt
    - Retrieve asteroid belt details
    - Update asteroid belt
    - Delete asteroid belt
    
    **Fields:**
    - Resource production rates
    - Orbital position
    """
    queryset = AsteroidBelt.objects.all()
    serializer_class = AsteroidBeltSerializer

class SystemViewSet(viewsets.ModelViewSet):
    """Manage star systems through the API.
    
    **Operations:**
    - List all systems
    - Create new system
    - Retrieve system details
    - Update system
    - Delete system
    - Add planet to system
    - Add asteroid belt to system
    
    **Constraints:**
    - Maximum of 5 orbital positions
    - Unique x,y coordinates within a game
    - Each orbit can only be occupied by one celestial body
    """
    queryset = System.objects.all()
    serializer_class = SystemSerializer

    @action(detail=True, methods=['post'])
    def add_planet(self, request, pk=None):
        """Add a planet to the system.
        
        **Process:**
        1. Validate planet data
        2. Create planet
        3. Validate system constraints
        4. Return created planet
        
        **Validation:**
        - Orbital position must be unique
        - Total orbits cannot exceed MAX_ORBITS
        """
        system = self.get_object()
        serializer = PlanetSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                planet = serializer.save(system=system)
                system.clean()  # Validate system constraints
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_asteroid_belt(self, request, pk=None):
        """Add an asteroid belt to the system.
        
        **Process:**
        1. Validate asteroid belt data
        2. Create asteroid belt
        3. Validate system constraints
        4. Return created asteroid belt
        
        **Validation:**
        - Orbital position must be unique
        - Total orbits cannot exceed MAX_ORBITS
        """
        system = self.get_object()
        serializer = AsteroidBeltSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                belt = serializer.save(system=system)
                system.clean()  # Validate system constraints
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
