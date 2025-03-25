from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from research.models import Technology, EmpireTechnology
from play.models import Player, Race, Empire


class TechnologyAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.tech_list_url = reverse('technology-list')
        self.tech1 = Technology.objects.create(
            name="Basic Mining",
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

    def tearDown(self):
        """Clean up test data"""
        Technology.objects.all().delete()

    def test_list_technologies(self):
        """Test retrieving a list of technologies"""
        response = self.client.get(self.tech_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_technology(self):
        """Test creating a new technology"""
        data = {
            'name': 'Laser Weapons',
            'description': 'Basic laser weapon technology',
            'category': Technology.Category.MILITARY,
            'cost': 150
        }
        response = self.client.post(self.tech_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Laser Weapons')
        self.assertEqual(response.data['category'], Technology.Category.MILITARY)

    def test_retrieve_technology(self):
        """Test retrieving a specific technology"""
        url = reverse('technology-detail', args=[self.tech1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Basic Mining')

    def test_add_prerequisite(self):
        """Test adding a prerequisite technology"""
        url = reverse('technology-add-prerequisite', args=[self.tech2.id])
        data = {'prerequisite_id': self.tech1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.tech1.id, [t for t in response.data['prerequisites']])

    def test_remove_prerequisite(self):
        """Test removing a prerequisite technology"""
        # First add a prerequisite
        self.tech2.prerequisites.add(self.tech1)
        
        url = reverse('technology-remove-prerequisite', args=[self.tech2.id])
        data = {'prerequisite_id': self.tech1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.tech1.id, [t for t in response.data['prerequisites']])


class EmpireTechnologyAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.empire_tech_list_url = reverse('empiretechnology-list')
        
        # Create player and race
        self.player = Player.objects.create(player_type=Player.PlayerType.HUMAN)
        self.race = Race.objects.create(name="Test Race")
        self.empire = Empire.objects.create(
            name="Test Empire",
            player=self.player,
            race=self.race
        )
        
        # Create technologies
        self.tech1 = Technology.objects.create(
            name="Test Technology 1",
            description="Test technology 1",
            category=Technology.Category.SCIENCE,
            cost=100
        )
        self.tech2 = Technology.objects.create(
            name="Test Technology 2",
            description="Test technology 2",
            category=Technology.Category.SCIENCE,
            cost=200
        )
        
        # Create empire technology
        self.empire_tech = EmpireTechnology.objects.create(
            empire=self.empire,
            technology=self.tech1,
            research_points=50
        )

    def tearDown(self):
        """Clean up test data"""
        EmpireTechnology.objects.all().delete()
        Technology.objects.all().delete()
        Empire.objects.all().delete()
        Race.objects.all().delete()
        Player.objects.all().delete()

    def test_list_empire_technologies(self):
        """Test retrieving a list of empire technologies"""
        response = self.client.get(self.empire_tech_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_empire_technology(self):
        """Test creating a new empire technology"""
        data = {
            'empire_id': self.empire.id,
            'technology_id': self.tech2.id,  # Use tech2 to avoid duplicate
            'research_points': 0
        }
        response = self.client.post(self.empire_tech_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['research_points'], '0.00')

    def test_retrieve_empire_technology(self):
        """Test retrieving a specific empire technology"""
        url = reverse('empiretechnology-detail', args=[self.empire_tech.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['research_points'], '50.00')

    def test_add_research_points(self):
        """Test adding research points to an empire technology"""
        url = reverse('empiretechnology-add-research-points', args=[self.empire_tech.id])
        data = {'points': 25}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['research_points'], '75.00')

    def test_prerequisites_status(self):
        """Test getting prerequisites status for an empire technology"""
        # Create a prerequisite technology
        prereq_tech = Technology.objects.create(
            name="Prerequisite Tech",
            description="Prerequisite technology",
            category=Technology.Category.SCIENCE,
            cost=50
        )
        self.tech1.prerequisites.add(prereq_tech)
        
        # Create empire technology for prerequisite
        prereq_empire_tech = EmpireTechnology.objects.create(
            empire=self.empire,
            technology=prereq_tech,
            research_points=25
        )
        
        url = reverse('empiretechnology-prerequisites-status', args=[self.empire_tech.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['technology_id'], prereq_tech.id)
        self.assertEqual(response.data[0]['research_points'], '25.00')
        self.assertEqual(response.data[0]['cost'], 50)
        self.assertFalse(response.data[0]['is_complete']) 