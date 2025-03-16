from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PlayerViewSet, RaceViewSet, EmpireViewSet, GameViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'races', RaceViewSet)
router.register(r'empires', EmpireViewSet)
router.register(r'games', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
