"""
Test cases for celestial API endpoints.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from ..models import Planet, Star


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

class StarAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.star = Star.objects.create(star_type='blue')
        self.list_url = reverse('star-list')
        self.detail_url = reverse('star-detail', args=[self.star.id])

    def test_list_stars(self):
        """Test retrieving a list of stars"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['star_type'], 'blue')

    def test_create_star(self):
        """Test creating a new star"""
        data = {'star_type': 'yellow'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Star.objects.count(), 2)
        self.assertEqual(response.data['star_type'], 'yellow')

    def test_create_star_invalid_type(self):
        """Test creating a star with invalid type fails"""
        data = {'star_type': 'invalid'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_star(self):
        """Test retrieving a single star"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['star_type'], 'blue')

    def test_update_star(self):
        """Test updating a star"""
        data = {'star_type': 'white'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['star_type'], 'white')
        self.star.refresh_from_db()
        self.assertEqual(self.star.star_type, 'white')

    def test_delete_star(self):
        """Test deleting a star"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Star.objects.count(), 0) 