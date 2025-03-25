from django.test import TestCase
from django.core.exceptions import ValidationError
from research.models import Technology


class TechnologyModelTests(TestCase):
    """Test cases for the Technology model."""

    def setUp(self):
        """Create base test data."""
        self.tech1 = Technology.objects.create(
            name="Mining I",
            description="Basic mining technology",
            category=Technology.Category.RESOURCES
        )
        self.tech2 = Technology.objects.create(
            name="Advanced Mining",
            description="Advanced mining technology",
            category=Technology.Category.RESOURCES
        )

    def test_technology_creation(self):
        """Test that a technology can be created with valid data."""
        tech = Technology.objects.create(
            name="Laser Weapons",
            description="Basic laser weapon technology",
            category=Technology.Category.MILITARY
        )
        self.assertEqual(tech.name, "Laser Weapons")
        self.assertEqual(tech.category, Technology.Category.MILITARY)

    def test_technology_str_representation(self):
        """Test the string representation of Technology."""
        self.assertEqual(
            str(self.tech1),
            "Mining I (Resources)"
        )

    def test_prerequisites(self):
        """Test adding prerequisites to a technology."""
        self.tech2.prerequisites.add(self.tech1)
        self.assertIn(self.tech1, self.tech2.prerequisites.all())
        self.assertNotIn(self.tech2, self.tech1.prerequisites.all())

    def test_invalid_category(self):
        """Test that invalid categories are rejected."""
        with self.assertRaises(ValidationError):
            tech = Technology(
                name="Invalid Tech",
                description="Test",
                category="INVALID"
            )
            tech.full_clean()

    def tearDown(self):
        """Clean up test data."""
        Technology.objects.all().delete() 