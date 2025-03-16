"""
Test cases for celestial API endpoints.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
from django.core.exceptions import ValidationError
from ..models import Planet, Star, AsteroidBelt, System


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
            exotic_storage_capacity=Decimal('125.75'),
            orbit=3
        )
        self.list_url = reverse('planet-list')
        self.detail_url = reverse('planet-detail', args=[self.planet.id])

    def tearDown(self):
        """Clean up test data"""
        Planet.objects.all().delete()

    def test_list_planets(self):
        """Test retrieving a list of planets"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['mineral_production'], '75.50')
        self.assertEqual(response.data[0]['orbit'], 3)

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
            'exotic_storage_capacity': '135.75',
            'orbit': 2
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Planet.objects.count(), 2)
        self.assertEqual(response.data['mineral_production'], '80.50')
        self.assertEqual(response.data['orbit'], 2)

    def test_retrieve_planet(self):
        """Test retrieving a single planet"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mineral_production'], '75.50')
        self.assertEqual(response.data['orbit'], 3)

    def test_update_planet(self):
        """Test updating a planet"""
        data = {
            'mineral_production': '90.50',
            'orbit': 4
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mineral_production'], '90.50')
        self.assertEqual(response.data['orbit'], 4)
        self.planet.refresh_from_db()
        self.assertEqual(self.planet.mineral_production, Decimal('90.50'))
        self.assertEqual(self.planet.orbit, 4)

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

    def tearDown(self):
        """Clean up test data"""
        Star.objects.all().delete()

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

class AsteroidBeltAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.belt = AsteroidBelt.objects.create(
            mineral_production=Decimal('75.5'),
            organic_production=Decimal('25.25'),
            radioactive_production=Decimal('60.75'),
            exotic_production=Decimal('40.25'),
            orbit=4
        )
        self.list_url = reverse('asteroidbelt-list')
        self.detail_url = reverse('asteroidbelt-detail', args=[self.belt.id])

    def tearDown(self):
        """Clean up test data"""
        AsteroidBelt.objects.all().delete()

    def test_list_asteroid_belts(self):
        """Test retrieving a list of asteroid belts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['mineral_production'], '75.50')
        self.assertEqual(response.data[0]['orbit'], 4)

    def test_create_asteroid_belt(self):
        """Test creating a new asteroid belt"""
        data = {
            'mineral_production': '80.50',
            'organic_production': '30.25',
            'radioactive_production': '65.75',
            'exotic_production': '45.25',
            'orbit': 2
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AsteroidBelt.objects.count(), 2)
        self.assertEqual(response.data['mineral_production'], '80.50')
        self.assertEqual(response.data['orbit'], 2)

    def test_retrieve_asteroid_belt(self):
        """Test retrieving a single asteroid belt"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mineral_production'], '75.50')
        self.assertEqual(response.data['orbit'], 4)

    def test_update_asteroid_belt(self):
        """Test updating an asteroid belt"""
        data = {
            'mineral_production': '90.50',
            'orbit': 5
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mineral_production'], '90.50')
        self.assertEqual(response.data['orbit'], 5)
        self.belt.refresh_from_db()
        self.assertEqual(self.belt.mineral_production, Decimal('90.50'))
        self.assertEqual(self.belt.orbit, 5)

    def test_delete_asteroid_belt(self):
        """Test deleting an asteroid belt"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AsteroidBelt.objects.count(), 0)

class SystemAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.star = Star.objects.create(star_type='yellow')
        self.system = System.objects.create(
            x=1,
            y=1,
            star=self.star
        )
        self.list_url = reverse('system-list')
        self.detail_url = reverse('system-detail', args=[self.system.id])
        self.add_planet_url = reverse('system-add-planet', args=[self.system.id])
        self.add_asteroid_belt_url = reverse('system-add-asteroid-belt', args=[self.system.id])

    def tearDown(self):
        """Clean up test data"""
        System.objects.all().delete()
        Star.objects.all().delete()
        Planet.objects.all().delete()
        AsteroidBelt.objects.all().delete()

    def test_list_systems(self):
        """Test retrieving a list of systems"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['x'], 1)
        self.assertEqual(response.data[0]['y'], 1)
        self.assertEqual(response.data[0]['star']['star_type'], 'yellow')

    def test_create_system(self):
        """Test creating a new system"""
        data = {
            'x': 2,
            'y': 2,
            'star': {'star_type': 'blue'}
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(System.objects.count(), 2)
        self.assertEqual(response.data['x'], 2)
        self.assertEqual(response.data['y'], 2)
        self.assertEqual(response.data['star']['star_type'], 'blue')

    def test_create_system_duplicate_coordinates(self):
        """Test creating a system with duplicate coordinates fails"""
        data = {
            'x': 1,
            'y': 1,
            'star': {'star_type': 'blue'}
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_system(self):
        """Test retrieving a single system"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['x'], 1)
        self.assertEqual(response.data['y'], 1)
        self.assertEqual(response.data['star']['star_type'], 'yellow')

    def test_update_system(self):
        """Test updating a system"""
        data = {
            'x': 3,
            'y': 3,
            'star': {'star_type': 'white'}
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['x'], 3)
        self.assertEqual(response.data['y'], 3)
        self.assertEqual(response.data['star']['star_type'], 'white')

    def test_delete_system(self):
        """Test deleting a system"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(System.objects.count(), 0)

    def test_add_planet(self):
        """Test adding a planet to a system"""
        data = {
            'mineral_production': '80.50',
            'organic_production': '30.25',
            'radioactive_production': '65.75',
            'exotic_production': '45.25',
            'mineral_storage_capacity': '160.50',
            'organic_storage_capacity': '210.75',
            'radioactive_storage_capacity': '185.25',
            'exotic_storage_capacity': '135.75',
            'orbit': 1
        }
        response = self.client.post(self.add_planet_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.system.planets.count(), 1)
        self.assertEqual(self.system.planets.first().orbit, 1)

    def test_add_asteroid_belt(self):
        """Test adding an asteroid belt to a system"""
        data = {
            'mineral_production': '80.50',
            'organic_production': '30.25',
            'radioactive_production': '65.75',
            'exotic_production': '45.25',
            'orbit': 2
        }
        response = self.client.post(self.add_asteroid_belt_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.system.asteroid_belts.count(), 1)
        self.assertEqual(self.system.asteroid_belts.first().orbit, 2)

    def test_max_orbits_constraint(self):
        """Test that adding more than MAX_ORBITS celestial bodies fails"""
        # Add MAX_ORBITS planets
        for i in range(1, System.MAX_ORBITS + 1):
            data = {
                'mineral_production': '80.50',
                'organic_production': '30.25',
                'radioactive_production': '65.75',
                'exotic_production': '45.25',
                'mineral_storage_capacity': '160.50',
                'organic_storage_capacity': '210.75',
                'radioactive_storage_capacity': '185.25',
                'exotic_storage_capacity': '135.75',
                'orbit': i
            }
            response = self.client.post(self.add_planet_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to add one more planet
        data['orbit'] = System.MAX_ORBITS + 1
        response = self.client.post(self.add_planet_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_orbit_constraint(self):
        """Test that adding a celestial body to an occupied orbit fails"""
        # Add a planet
        planet_data = {
            'mineral_production': '80.50',
            'organic_production': '30.25',
            'radioactive_production': '65.75',
            'exotic_production': '45.25',
            'mineral_storage_capacity': '160.50',
            'organic_storage_capacity': '210.75',
            'radioactive_storage_capacity': '185.25',
            'exotic_storage_capacity': '135.75',
            'orbit': 1
        }
        response = self.client.post(self.add_planet_url, planet_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to add an asteroid belt in the same orbit
        belt_data = {
            'mineral_production': '80.50',
            'organic_production': '30.25',
            'radioactive_production': '65.75',
            'exotic_production': '45.25',
            'orbit': 1
        }
        response = self.client.post(self.add_asteroid_belt_url, belt_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 