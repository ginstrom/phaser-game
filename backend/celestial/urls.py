from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanetViewSet, StarViewSet

router = DefaultRouter()
router.register(r'planets', PlanetViewSet)
router.register(r'stars', StarViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 