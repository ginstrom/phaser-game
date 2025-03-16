from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from play.models import Player, Race, Empire, Game
from celestial.models import System, Star
from play.start import start_game, create_star_systems, create_computer_empires, GalaxySize

class GameStartModuleTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.race = Race.objects.create(name="Test Race")
        self.valid_data = {
            'player_empire_name': 'Test Empire',
            'computer_empire_count': 2,
            'galaxy_size': 'tiny'
        }

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
        self.assertEqual(
            System.objects.filter(game=game).count(),
            GalaxySize.SYSTEM_COUNTS[self.valid_data['galaxy_size']]
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

    def test_start_game_invalid_galaxy_size(self):
        """Test starting a game with invalid galaxy size"""
        invalid_data = self.valid_data.copy()
        invalid_data['galaxy_size'] = 'invalid_size'
        
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


class GameStartAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.start_url = reverse('game-start')
        self.valid_data = {
            'player_empire_name': 'Test Empire',
            'computer_empire_count': 2,
            'galaxy_size': 'tiny'
        }

    def test_start_game_api_valid_data(self):
        """Test starting a game through API with valid data"""
        response = self.client.post(self.start_url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)
        
        # Verify response data
        self.assertEqual(response.data['turn'], 1)
        
        # Verify game was created with correct properties
        game = Game.objects.first()
        self.assertEqual(
            System.objects.filter(game=game).count(),
            GalaxySize.SYSTEM_COUNTS[self.valid_data['galaxy_size']]
        )
        self.assertEqual(
            Empire.objects.filter(game=game).count(),
            self.valid_data['computer_empire_count'] + 1
        )

    def test_start_game_api_missing_fields(self):
        """Test starting a game with missing required fields"""
        # Test each required field
        required_fields = ['player_empire_name', 'computer_empire_count', 'galaxy_size']
        
        for field in required_fields:
            invalid_data = self.valid_data.copy()
            del invalid_data[field]
            
            response = self.client.post(self.start_url, invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('error', response.data)
            self.assertIn(field, response.data['error'])

    def test_start_game_api_invalid_galaxy_size(self):
        """Test starting a game with invalid galaxy size"""
        invalid_data = self.valid_data.copy()
        invalid_data['galaxy_size'] = 'invalid_size'
        
        response = self.client.post(self.start_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Invalid galaxy size', response.data['error'])

    def test_start_game_api_different_galaxy_sizes(self):
        """Test starting games with different galaxy sizes"""
        for size, count in GalaxySize.SYSTEM_COUNTS.items():
            data = self.valid_data.copy()
            data['galaxy_size'] = size
            
            response = self.client.post(self.start_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
            game = Game.objects.latest('id')
            self.assertEqual(System.objects.filter(game=game).count(), count)

    def tearDown(self):
        """Clean up test data"""
        Game.objects.all().delete()
        Empire.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
        System.objects.all().delete()
        Star.objects.all().delete() 