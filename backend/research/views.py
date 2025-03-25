from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal
from research.models import Technology, EmpireTechnology
from research.serializers import TechnologySerializer, EmpireTechnologySerializer


class TechnologyViewSet(viewsets.ModelViewSet):
    """ViewSet for Technology model.
    
    Provides CRUD operations for technologies and additional actions for managing prerequisites.
    """
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

    @action(detail=True, methods=['post'])
    def add_prerequisite(self, request, pk=None):
        """Add a prerequisite technology to this technology."""
        technology = self.get_object()
        prerequisite_id = request.data.get('prerequisite_id')
        
        if not prerequisite_id:
            return Response(
                {'error': 'prerequisite_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            prerequisite = Technology.objects.get(id=prerequisite_id)
            technology.prerequisites.add(prerequisite)
            return Response(self.get_serializer(technology).data)
        except Technology.DoesNotExist:
            return Response(
                {'error': 'Prerequisite technology not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_prerequisite(self, request, pk=None):
        """Remove a prerequisite technology from this technology."""
        technology = self.get_object()
        prerequisite_id = request.data.get('prerequisite_id')
        
        if not prerequisite_id:
            return Response(
                {'error': 'prerequisite_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            prerequisite = Technology.objects.get(id=prerequisite_id)
            technology.prerequisites.remove(prerequisite)
            return Response(self.get_serializer(technology).data)
        except Technology.DoesNotExist:
            return Response(
                {'error': 'Prerequisite technology not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class EmpireTechnologyViewSet(viewsets.ModelViewSet):
    """ViewSet for EmpireTechnology model.
    
    Provides CRUD operations for empire technology research and additional actions for managing research progress.
    """
    queryset = EmpireTechnology.objects.all()
    serializer_class = EmpireTechnologySerializer

    @action(detail=True, methods=['post'])
    def add_research_points(self, request, pk=None):
        """Add research points to an empire's technology research."""
        empire_tech = self.get_object()
        points = request.data.get('points')
        
        if not points:
            return Response(
                {'error': 'points is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            points = Decimal(str(points))
            if points <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'points must be a positive number'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        with transaction.atomic():
            empire_tech.research_points += points
            empire_tech.save()
            
        return Response(self.get_serializer(empire_tech).data)

    @action(detail=True, methods=['get'])
    def prerequisites_status(self, request, pk=None):
        """Get the status of prerequisites for this technology research."""
        empire_tech = self.get_object()
        prerequisites = empire_tech.technology.prerequisites.all()
        
        status_data = []
        for prereq in prerequisites:
            try:
                prereq_research = EmpireTechnology.objects.get(
                    empire=empire_tech.empire,
                    technology=prereq
                )
                status_data.append({
                    'technology_id': prereq.id,
                    'name': prereq.name,
                    'is_complete': prereq_research.is_complete,
                    'research_points': str(prereq_research.research_points),
                    'cost': prereq.cost
                })
            except EmpireTechnology.DoesNotExist:
                status_data.append({
                    'technology_id': prereq.id,
                    'name': prereq.name,
                    'is_complete': False,
                    'research_points': '0.00',
                    'cost': prereq.cost
                })
                
        return Response(status_data)
