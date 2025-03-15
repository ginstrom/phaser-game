"""
Test cases for celestial API endpoints.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from ..models import Planet


class PlanetAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.planet = Planet.objects.create(
            mineral_production=Decimal('75.5'),
            organic_production=Decimal('25.25'),
            radioactive_production=Decimal('60.75'),
            exotic_production=Decimal('40.25'),
            mineral_storage_capacity=Decimal('150.5'),
            organic_storage_capacity=Decimal('200.75'),
            radioactive_storage_capacity=Decimal('175.25'),
            exotic_storage_capacity=Decimal('125.75')
        )
        self.list_url = reverse('planet-list')
        self.detail_url = reverse('planet-detail', args=[self.planet.id])

    def test_list_planets(self):
        """Test retrieving a list of planets"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['mineral_production'], '75.50')

    def test_create_planet(self):
        """Test creating a new planet"""
        data = {
            'mineral_production': '80.50',
            'organic_production': '30.25',
            'radioactive_production': '65.75',
            'exotic_production': '45.25',
            'mineral_storage_capacity': '160.50',
            'organic_storage_capacity': '210.75',
            'radioactive_storage_capacity': '185.25',
            'exotic_storage_capacity': '135.75'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Planet.objects.count(), 2)
        self.assertEqual(response.data['mineral_production'], '80.50')

    def test_retrieve_planet(self):
        """Test retrieving a single planet"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mineral_production'], '75.50')

    def test_update_planet(self):
        """Test updating a planet"""
        data = {'mineral_production': '90.50'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mineral_production'], '90.50')
        self.planet.refresh_from_db()
        self.assertEqual(self.planet.mineral_production, Decimal('90.50'))

    def test_delete_planet(self):
        """Test deleting a planet"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Planet.objects.count(), 0) 