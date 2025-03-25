from rest_framework import serializers
from research.models import Technology, EmpireTechnology
from play.serializers import EmpireSerializer
from play.models import Empire


class TechnologySerializer(serializers.ModelSerializer):
    """Serializer for Technology model.
    
    Handles conversion of Technology instances to/from JSON for API responses.
    Includes related prerequisites information.
    """
    prerequisites = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text="Technologies that must be researched before this one"
    )
    prerequisite_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        source='prerequisites',
        queryset=Technology.objects.all(),
        write_only=True,
        required=False,
        help_text="IDs of prerequisite technologies"
    )

    class Meta:
        model = Technology
        fields = [
            'id', 'name', 'description', 'category', 'cost',
            'prerequisites', 'prerequisite_ids'
        ]
        read_only_fields = ['id']


class EmpireTechnologySerializer(serializers.ModelSerializer):
    """Serializer for EmpireTechnology model.
    
    Handles conversion of EmpireTechnology instances to/from JSON for API responses.
    Includes related technology and empire information.
    """
    technology = TechnologySerializer(read_only=True)
    technology_id = serializers.PrimaryKeyRelatedField(
        queryset=Technology.objects.all(),
        source='technology',
        write_only=True,
        help_text="The technology being researched"
    )
    empire = EmpireSerializer(read_only=True)
    empire_id = serializers.PrimaryKeyRelatedField(
        queryset=Empire.objects.all(),
        source='empire',
        write_only=True,
        help_text="The empire researching the technology"
    )

    class Meta:
        model = EmpireTechnology
        fields = [
            'id', 'technology', 'technology_id', 'empire', 'empire_id',
            'research_points', 'is_complete'
        ]
        read_only_fields = ['id', 'is_complete'] 