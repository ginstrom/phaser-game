from django.shortcuts import render
from rest_framework import viewsets
from .models import Planet
from .serializers import PlanetSerializer

# Create your views here.

class PlanetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows planets to be viewed or edited.
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
