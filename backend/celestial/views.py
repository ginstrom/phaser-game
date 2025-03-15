from django.shortcuts import render
from rest_framework import viewsets
from .models import Planet, Star
from .serializers import PlanetSerializer, StarSerializer

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
