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
    """
    API endpoint that allows planets to be viewed or edited.
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

class StarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stars to be viewed or edited.
    """
    queryset = Star.objects.all()
    serializer_class = StarSerializer

class AsteroidBeltViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows asteroid belts to be viewed or edited.
    """
    queryset = AsteroidBelt.objects.all()
    serializer_class = AsteroidBeltSerializer

class SystemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows star systems to be viewed or edited.
    
    A system consists of:
    - A single star
    - 0 to MAX_ORBITS (5) planets and/or asteroid belts
    - Unique x,y coordinates in the galaxy
    """
    queryset = System.objects.all()
    serializer_class = SystemSerializer

    @action(detail=True, methods=['post'])
    def add_planet(self, request, pk=None):
        """Add a planet to the system"""
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
        """Add an asteroid belt to the system"""
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
