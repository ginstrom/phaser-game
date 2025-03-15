from django.shortcuts import render
from rest_framework import viewsets
from .models import Player, Race, Empire
from .serializers import PlayerSerializer, RaceSerializer, EmpireSerializer

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
