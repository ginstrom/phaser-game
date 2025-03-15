from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanetViewSet, StarViewSet, AsteroidBeltViewSet

router = DefaultRouter()
router.register(r'planets', PlanetViewSet)
router.register(r'stars', StarViewSet)
router.register(r'asteroid-belts', AsteroidBeltViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 