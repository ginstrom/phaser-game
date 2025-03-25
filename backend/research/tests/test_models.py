from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction
from research.models import Technology, EmpireTechnology
from play.models import Empire, Player, Race


class TechnologyModelTests(TestCase):
    """Test cases for the Technology model."""

    def setUp(self):
        """Create base test data."""
        self.tech1 = Technology.objects.create(
            name="Mining I",
            description="Basic mining technology",
            category=Technology.Category.RESOURCES,
            cost=100
        )
        self.tech2 = Technology.objects.create(
            name="Advanced Mining",
            description="Advanced mining technology",
            category=Technology.Category.RESOURCES,
            cost=200
        )

    def test_technology_creation(self):
        """Test that a technology can be created with valid data."""
        tech = Technology.objects.create(
            name="Laser Weapons",
            description="Basic laser weapon technology",
            category=Technology.Category.MILITARY,
            cost=150
        )
        self.assertEqual(tech.name, "Laser Weapons")
        self.assertEqual(tech.category, Technology.Category.MILITARY)
        self.assertEqual(tech.cost, 150)

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
                category="INVALID",
                cost=100
            )
            tech.full_clean()

    def test_default_cost(self):
        """Test that cost defaults to 100 if not specified."""
        tech = Technology.objects.create(
            name="Test Tech",
            description="Test technology",
            category=Technology.Category.SCIENCE
        )
        self.assertEqual(tech.cost, 100)

    def tearDown(self):
        """Clean up test data."""
        Technology.objects.all().delete()


class EmpireTechnologyModelTests(TestCase):
    """Test cases for the EmpireTechnology model."""

    def setUp(self):
        """Create base test data."""
        self.player = Player.objects.create(
            player_type=Player.PlayerType.HUMAN
        )
        self.race = Race.objects.create(
            name="Test Race"
        )
        self.empire = Empire.objects.create(
            name="Test Empire",
            player=self.player,
            race=self.race
        )
        self.tech = Technology.objects.create(
            name="Test Technology",
            description="Test technology",
            category=Technology.Category.SCIENCE,
            cost=100
        )
        self.empire_tech = EmpireTechnology.objects.create(
            empire=self.empire,
            technology=self.tech,
            research_points=50
        )

    def test_empire_technology_creation(self):
        """Test that an EmpireTechnology can be created with valid data."""
        self.assertEqual(self.empire_tech.empire, self.empire)
        self.assertEqual(self.empire_tech.technology, self.tech)
        self.assertEqual(self.empire_tech.research_points, 50)

    def test_empire_technology_str_representation(self):
        """Test the string representation of EmpireTechnology."""
        self.assertEqual(
            str(self.empire_tech),
            "Test Empire - Test Technology"
        )

    def test_is_complete_property(self):
        """Test the is_complete property."""
        # Test incomplete technology
        self.assertFalse(self.empire_tech.is_complete)

        # Test complete technology
        self.empire_tech.research_points = 100
        self.empire_tech.save()
        self.assertTrue(self.empire_tech.is_complete)

        # Test technology with excess research points
        self.empire_tech.research_points = 150
        self.empire_tech.save()
        self.assertTrue(self.empire_tech.is_complete)

    def test_unique_together_constraint(self):
        """Test that an empire can't research the same technology twice."""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                EmpireTechnology.objects.create(
                    empire=self.empire,
                    technology=self.tech,
                    research_points=0
                )

    def tearDown(self):
        """Clean up test data."""
        try:
            EmpireTechnology.objects.all().delete()
            Technology.objects.all().delete()
            Empire.objects.all().delete()
            Race.objects.all().delete()
            Player.objects.all().delete()
        except Exception:
            # Ignore any errors during cleanup since the test database will be destroyed
            pass 