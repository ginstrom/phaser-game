from django.test import TestCase
from django.db import transaction
from play.models import Player, Race, Empire, Game
from celestial.models import Planet, AsteroidBelt, System, Star
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class PlayerModelTests(TestCase):
    def test_create_player_with_valid_type(self):
        """Test creating a player with valid player types"""
        # Test human player
        human_player = Player.objects.create(player_type=Player.PlayerType.HUMAN)
        self.assertEqual(human_player.player_type, 'human')

        # Test computer player
        computer_player = Player.objects.create(player_type=Player.PlayerType.COMPUTER)
        self.assertEqual(computer_player.player_type, 'computer')

    def test_default_player_type(self):
        """Test that default player type is human"""
        player = Player.objects.create()
        self.assertEqual(player.player_type, Player.PlayerType.HUMAN)

    def test_string_representation(self):
        """Test the string representation of Player model"""
        player = Player.objects.create(player_type=Player.PlayerType.COMPUTER)
        self.assertIn('computer player', str(player))
        self.assertIn(str(player.id), str(player))

    def tearDown(self):
        """Clean up test data"""
        Player.objects.all().delete()


class RaceModelTests(TestCase):
    def test_create_race(self):
        """Test creating a race with a name"""
        race = Race.objects.create(name="Humans")
        self.assertEqual(race.name, "Humans")
        self.assertEqual(str(race), "Humans")

    def test_unique_name_constraint(self):
        """Test that race names must be unique"""
        Race.objects.create(name="Humans")
        with transaction.atomic():
            with self.assertRaises(Exception):
                Race.objects.create(name="Humans")

    def tearDown(self):
        """Clean up test data"""
        Race.objects.all().delete()


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
        self.empire.planets.add(self.planet1, self.planet2)
        self.empire.asteroid_belts.add(self.asteroid_belt)

    def test_create_empire(self):
        """Test creating an empire with basic attributes"""
        self.assertEqual(self.empire.name, "Test Empire")
        self.assertEqual(self.empire.player, self.player)
        self.assertEqual(self.empire.race, self.race)
        self.assertEqual(str(self.empire), f"Test Empire ({self.race.name})")

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

    def tearDown(self):
        """Clean up test data"""
        Empire.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
        System.objects.all().delete()  # This will cascade delete planets and asteroid belts
        Star.objects.all().delete()


class GameModelTests(TestCase):
    def setUp(self):
        # Create a game
        self.game = Game.objects.create(turn=1)
        
        # Create players
        self.player1 = Player.objects.create(player_type=Player.PlayerType.HUMAN)
        self.player2 = Player.objects.create(player_type=Player.PlayerType.COMPUTER)
        
        # Create a race
        self.race = Race.objects.create(name="Test Race")
        
        # Create empires
        self.empire1 = Empire.objects.create(
            name="Empire 1",
            player=self.player1,
            race=self.race,
            game=self.game
        )
        self.empire2 = Empire.objects.create(
            name="Empire 2",
            player=self.player2,
            race=self.race,
            game=self.game
        )
        
        # Create stars and systems
        star1 = Star.objects.create(star_type=Star.StarType.YELLOW)
        star2 = Star.objects.create(star_type=Star.StarType.BLUE)
        
        self.system1 = System.objects.create(
            x=0,
            y=0,
            star=star1,
            game=self.game
        )
        self.system2 = System.objects.create(
            x=1,
            y=1,
            star=star2,
            game=self.game
        )

    def test_game_creation(self):
        """Test that a game can be created with valid data"""
        self.assertEqual(self.game.turn, 1)
        self.assertEqual(self.game.empires.count(), 2)
        self.assertEqual(self.game.systems.count(), 2)
        self.assertEqual(str(self.game), f"Game {self.game.id} (Turn 1)")
        
        # Validate should pass with 2 empires and 2 systems
        self.game.clean()

    def test_game_minimum_empires(self):
        """Test that a game requires at least 2 empires"""
        # Delete one empire
        self.empire2.delete()
        
        # Game should raise validation error
        with self.assertRaises(ValidationError):
            self.game.clean()

    def test_game_minimum_systems(self):
        """Test that a game requires at least 2 systems"""
        # Delete one system
        self.system2.delete()
        
        # Game should raise validation error
        with self.assertRaises(ValidationError):
            self.game.clean()

    def test_system_unique_coordinates_per_game(self):
        """Test that system coordinates must be unique within a game"""
        # Try to create another system with same coordinates in same game
        star3 = Star.objects.create(star_type=Star.StarType.WHITE)
        
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                System.objects.create(
                    x=0,
                    y=0,
                    star=star3,
                    game=self.game
                )

    def test_empire_game_relationship(self):
        """Test that empires belong to exactly one game"""
        # Create another game
        game2 = Game.objects.create(turn=1)
        
        # Try to move empire to another game
        self.empire1.game = game2
        self.empire1.save()
        
        # Verify empire is now in game2
        self.empire1.refresh_from_db()
        self.assertEqual(self.empire1.game, game2)
        
        # Verify original game fails validation
        with self.assertRaises(ValidationError):
            self.game.clean()

    def tearDown(self):
        """Clean up test data"""
        System.objects.all().delete()
        Star.objects.all().delete()
        Empire.objects.all().delete()
        Game.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
