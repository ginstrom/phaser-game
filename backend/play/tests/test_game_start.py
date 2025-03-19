from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from play.models import Player, Race, Empire, Game
from celestial.models import System, Star, Planet, AsteroidBelt
from play.start import start_game, create_star_systems, create_computer_empires, GalaxySize, create_star_system, assign_colony_planets, GALAXY_SIZE_SYSTEM_COUNTS

class GameStartModuleTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.race = Race.objects.create(name="Test Race")
        self.valid_data = {
            'player_empire_name': 'Test Empire',
            'computer_empire_count': 2,
            'galaxy_size': GalaxySize.TINY.value
        }

    def test_create_star_system(self):
        """Test creating a single star system"""
        game = Game.objects.create(turn=1)
        x, y = 10, 20
        
        system = create_star_system(game, x, y)
        
        # Test system properties
        self.assertEqual(system.x, x)
        self.assertEqual(system.y, y)
        self.assertEqual(system.game, game)
        self.assertEqual(system.star.star_type, Star.StarType.YELLOW)
        self.assertEqual(System.objects.filter(game=game).count(), 1)
        
        # Test planet creation
        planet = system.planets.first()
        self.assertEqual(planet.orbit, 1)
        self.assertEqual(planet.mineral_production, 75)
        self.assertEqual(planet.organic_production, 75)
        self.assertEqual(planet.radioactive_production, 25)
        self.assertEqual(planet.exotic_production, 25)
        self.assertEqual(planet.mineral_storage_capacity, 150)
        self.assertEqual(planet.organic_storage_capacity, 150)
        self.assertEqual(planet.radioactive_storage_capacity, 100)
        self.assertEqual(planet.exotic_storage_capacity, 100)
        
        # Test asteroid belt creation
        asteroid_belt = system.asteroid_belts.first()
        self.assertEqual(asteroid_belt.orbit, 2)
        self.assertEqual(asteroid_belt.mineral_production, 100)
        self.assertEqual(asteroid_belt.organic_production, 25)
        self.assertEqual(asteroid_belt.radioactive_production, 75)
        self.assertEqual(asteroid_belt.exotic_production, 50)

    def test_create_star_systems(self):
        """Test creating star systems for a game"""
        game = Game.objects.create(turn=1)
        systems = create_star_systems(game, 3)
        
        self.assertEqual(len(systems), 3)
        self.assertEqual(System.objects.filter(game=game).count(), 3)
        
        # Test system coordinates
        for i, system in enumerate(systems):
            self.assertEqual(system.x, i * 2)
            self.assertEqual(system.y, i * 2)
            self.assertEqual(system.star.star_type, Star.StarType.YELLOW)

    def test_create_computer_empires(self):
        """Test creating computer empires"""
        game = Game.objects.create(turn=1)
        empires = create_computer_empires(game, 3, self.race)
        
        self.assertEqual(len(empires), 3)
        self.assertEqual(Empire.objects.filter(game=game).count(), 3)
        
        # Test empire properties
        for i, empire in enumerate(empires):
            self.assertEqual(empire.name, f"Computer Empire {i+1}")
            self.assertEqual(empire.race, self.race)
            self.assertEqual(empire.player.player_type, Player.PlayerType.COMPUTER)

    def test_start_game_valid_data(self):
        """Test starting a game with valid data"""
        game = start_game(self.valid_data)
        
        # Test game properties
        self.assertEqual(game.turn, 1)
        
        # Test systems created
        # For TINY galaxy (2 systems) with 3 empires (1 human + 2 computer),
        # we expect 3 systems total (1 extra created for colony assignment)
        expected_systems = max(
            GALAXY_SIZE_SYSTEM_COUNTS[GalaxySize(self.valid_data['galaxy_size'])],
            self.valid_data['computer_empire_count'] + 1  # Total empires
        )
        self.assertEqual(
            System.objects.filter(game=game).count(),
            expected_systems
        )
        
        # Test empires created
        self.assertEqual(
            Empire.objects.filter(game=game).count(),
            self.valid_data['computer_empire_count'] + 1  # +1 for human empire
        )
        
        # Test human empire
        human_empire = Empire.objects.get(
            game=game,
            player__player_type=Player.PlayerType.HUMAN
        )
        self.assertEqual(human_empire.name, self.valid_data['player_empire_name'])
        
        # Test colony planet assignment
        human_planet = Planet.objects.filter(empire=human_empire).first()
        self.assertIsNotNone(human_planet)
        self.assertEqual(human_planet.orbit, 1)
        
        # Test computer empire colonies
        computer_empires = Empire.objects.filter(
            game=game,
            player__player_type=Player.PlayerType.COMPUTER
        )
        for empire in computer_empires:
            planet = Planet.objects.filter(empire=empire).first()
            self.assertIsNotNone(planet)
            self.assertEqual(planet.orbit, 1)

    def test_start_game_different_galaxy_sizes(self):
        """Test starting games with different galaxy sizes"""
        for size in GalaxySize:
            data = self.valid_data.copy()
            data['galaxy_size'] = size.value
            
            game = start_game(data)
            
            # Test systems created
            # We expect at least enough systems for all empires
            expected_systems = max(
                GALAXY_SIZE_SYSTEM_COUNTS[size],
                data['computer_empire_count'] + 1  # Total empires
            )
            self.assertEqual(
                System.objects.filter(game=game).count(),
                expected_systems
            )
            
            # Clean up for next iteration
            game.delete()

    def test_start_game_invalid_data(self):
        """Test starting a game with invalid data"""
        # Test missing required fields
        with self.assertRaises(ValueError):
            start_game({})
        
        # Test invalid galaxy size
        invalid_data = self.valid_data.copy()
        invalid_data['galaxy_size'] = 'invalid_size'
        with self.assertRaises(ValueError):
            start_game(invalid_data)
        
        # Test negative computer empire count
        invalid_data = self.valid_data.copy()
        invalid_data['computer_empire_count'] = -1
        with self.assertRaises(ValueError):
            start_game(invalid_data)

    def tearDown(self):
        """Clean up test data"""
        Game.objects.all().delete()
        Empire.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
        System.objects.all().delete()
        Star.objects.all().delete()

class EmpireModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create player and race
        self.player = Player.objects.create(player_type=Player.PlayerType.HUMAN)
        self.race = Race.objects.create(name="Test Race")
        
        # Create a star system
        self.star = Star.objects.create(star_type=Star.StarType.YELLOW)
        self.system = System.objects.create(x=0, y=0, star=self.star)
        
        # Create planets
        self.planet1 = Planet.objects.create(
            system=self.system,
            orbit=1,
            mineral_storage_capacity=100,
            organic_storage_capacity=150,
            radioactive_storage_capacity=200,
            exotic_storage_capacity=250
        )
        self.planet2 = Planet.objects.create(
            system=self.system,
            orbit=2,
            mineral_storage_capacity=300,
            organic_storage_capacity=350,
            radioactive_storage_capacity=400,
            exotic_storage_capacity=450
        )
        
        # Create asteroid belt
        self.asteroid_belt = AsteroidBelt.objects.create(
            system=self.system,
            orbit=3,
            mineral_production=50,
            organic_production=60,
            radioactive_production=70,
            exotic_production=80
        )
        
        # Create empire
        self.empire = Empire.objects.create(
            name="Test Empire",
            player=self.player,
            race=self.race
        )
        
        # Add planets and asteroid belt to empire
        self.planet1.empire = self.empire
        self.planet1.save()
        self.planet2.empire = self.empire
        self.planet2.save()
        self.asteroid_belt.empire = self.empire
        self.asteroid_belt.save()

    def test_empire_planets(self):
        """Test empire's relationship with planets"""
        self.assertEqual(self.empire.planets.count(), 2)
        self.assertIn(self.planet1, self.empire.planets.all())
        self.assertIn(self.planet2, self.empire.planets.all())

    def test_empire_asteroid_belts(self):
        """Test empire's relationship with asteroid belts"""
        self.assertEqual(self.empire.asteroid_belts.count(), 1)
        self.assertIn(self.asteroid_belt, self.empire.asteroid_belts.all())

    def test_resource_capacities(self):
        """Test empire's resource capacity calculations"""
        # Expected values are sum of both planets' capacities
        self.assertEqual(self.empire.mineral_capacity, 400)  # 100 + 300
        self.assertEqual(self.empire.organic_capacity, 500)  # 150 + 350
        self.assertEqual(self.empire.radioactive_capacity, 600)  # 200 + 400
        self.assertEqual(self.empire.exotic_capacity, 700)  # 250 + 450

    def test_resource_storage(self):
        """Test empire's resource storage values"""
        # Test default values
        self.assertEqual(self.empire.mineral_storage, 0)
        self.assertEqual(self.empire.organic_storage, 0)
        self.assertEqual(self.empire.radioactive_storage, 0)
        self.assertEqual(self.empire.exotic_storage, 0)
        
        # Test setting storage values
        self.empire.mineral_storage = 100
        self.empire.organic_storage = 200
        self.empire.radioactive_storage = 300
        self.empire.exotic_storage = 400
        self.empire.save()
        
        # Refresh from database
        self.empire.refresh_from_db()
        
        self.assertEqual(self.empire.mineral_storage, 100)
        self.assertEqual(self.empire.organic_storage, 200)
        self.assertEqual(self.empire.radioactive_storage, 300)
        self.assertEqual(self.empire.exotic_storage, 400)

    def test_update_empire_planets(self):
        """Test updating empire's planets"""
        # Remove planet2 from empire
        self.planet2.empire = None
        self.planet2.save()
        
        # Check that only planet1 remains
        self.assertEqual(self.empire.planets.count(), 1)
        self.assertIn(self.planet1, self.empire.planets.all())
        
        # Check updated resource capacities
        self.assertEqual(self.empire.mineral_capacity, 100)
        self.assertEqual(self.empire.organic_capacity, 150)
        self.assertEqual(self.empire.radioactive_capacity, 200)
        self.assertEqual(self.empire.exotic_capacity, 250)

    def test_update_empire_asteroid_belts(self):
        """Test updating empire's asteroid belts"""
        # Remove asteroid belt from empire
        self.asteroid_belt.empire = None
        self.asteroid_belt.save()
        
        # Check that no asteroid belts remain
        self.assertEqual(self.empire.asteroid_belts.count(), 0)

    def tearDown(self):
        """Clean up test data"""
        Empire.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
        System.objects.all().delete()  # This will cascade delete planets and asteroid belts
        Star.objects.all().delete()

class GameStartAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.race = Race.objects.create(name="Test Race")
        self.valid_data = {
            'player_empire_name': 'Test Empire',
            'computer_empire_count': 2,
            'galaxy_size': GalaxySize.TINY.value
        }
        self.url = reverse('game-start')

    def test_start_game_api_valid_data(self):
        """Test starting a game through API with valid data"""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the created game
        game = Game.objects.get(id=response.data['id'])
        
        # Test game properties
        self.assertEqual(game.turn, 1)
        
        # Test systems created
        # For TINY galaxy (2 systems) with 3 empires (1 human + 2 computer),
        # we expect 3 systems total (1 extra created for colony assignment)
        expected_systems = max(
            GALAXY_SIZE_SYSTEM_COUNTS[GalaxySize(self.valid_data['galaxy_size'])],
            self.valid_data['computer_empire_count'] + 1  # Total empires
        )
        self.assertEqual(
            System.objects.filter(game=game).count(),
            expected_systems
        )
        
        # Test empires created
        self.assertEqual(
            Empire.objects.filter(game=game).count(),
            self.valid_data['computer_empire_count'] + 1  # +1 for human empire
        )
        
        # Test human empire
        human_empire = Empire.objects.get(
            game=game,
            player__player_type=Player.PlayerType.HUMAN
        )
        self.assertEqual(human_empire.name, self.valid_data['player_empire_name'])
        
        # Test colony planet assignment
        human_planet = Planet.objects.filter(empire=human_empire).first()
        self.assertIsNotNone(human_planet)
        self.assertEqual(human_planet.orbit, 1)
        
        # Test computer empire colonies
        computer_empires = Empire.objects.filter(
            game=game,
            player__player_type=Player.PlayerType.COMPUTER
        )
        for empire in computer_empires:
            planet = Planet.objects.filter(empire=empire).first()
            self.assertIsNotNone(planet)
            self.assertEqual(planet.orbit, 1)

    def test_start_game_api_different_galaxy_sizes(self):
        """Test starting games with different galaxy sizes"""
        for size in GalaxySize:
            data = self.valid_data.copy()
            data['galaxy_size'] = size.value
            
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
            # Get the created game
            game = Game.objects.get(id=response.data['id'])
            
            # Test systems created
            # We expect at least enough systems for all empires
            expected_systems = max(
                GALAXY_SIZE_SYSTEM_COUNTS[size],
                data['computer_empire_count'] + 1  # Total empires
            )
            self.assertEqual(
                System.objects.filter(game=game).count(),
                expected_systems
            )
            
            # Clean up for next iteration
            game.delete()

    def test_start_game_api_invalid_data(self):
        """Test starting a game through API with invalid data"""
        # Test missing required fields
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid galaxy size
        invalid_data = self.valid_data.copy()
        invalid_data['galaxy_size'] = 'invalid_size'
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test negative computer empire count
        invalid_data = self.valid_data.copy()
        invalid_data['computer_empire_count'] = -1
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        """Clean up test data"""
        Game.objects.all().delete()
        Empire.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
        System.objects.all().delete()
        Star.objects.all().delete() 