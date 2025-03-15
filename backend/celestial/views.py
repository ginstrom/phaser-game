from django.shortcuts import render
from rest_framework import viewsets
from .models import Planet, Star, AsteroidBelt
from .serializers import PlanetSerializer, StarSerializer, AsteroidBeltSerializer

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
