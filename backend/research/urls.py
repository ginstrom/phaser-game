from django.urls import path, include
from rest_framework.routers import DefaultRouter
from research.views import TechnologyViewSet, EmpireTechnologyViewSet

router = DefaultRouter()
router.register(r'technologies', TechnologyViewSet)
router.register(r'empire-technologies', EmpireTechnologyViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 