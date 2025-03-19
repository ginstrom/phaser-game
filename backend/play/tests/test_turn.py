"""Tests for the turn processing functionality in the game.

This module contains test cases for the turn processing system, which handles
the advancement of game turns and associated state changes. The tests verify
that turns are properly advanced, game state is correctly updated, and changes
are persisted to the database.
"""

from django.test import TestCase
from decimal import Decimal
from play.models import Game, Empire, Player, Race
from play.turn import process, calculate_resource_production, update_empire_resources
from celestial.models import Planet, AsteroidBelt, System, Star

class TurnProcessingTests(TestCase):
    """Test suite for turn processing functionality.
    
    This test suite verifies the core turn processing mechanics including:
    - Turn counter advancement
    - Game state persistence
    - Multiple turn processing
    - Return value validation
    """

    def setUp(self):
        """Initialize test data by creating a new game instance.
        
        Creates a fresh game with turn counter set to 0 before each test.
        """
        self.game = Game.objects.create(turn=0)
        
        # Create test player and race
        self.player = Player.objects.create()
        self.race = Race.objects.create(name="Test Race")
        
        # Create test empire
        self.empire = Empire.objects.create(
            name="Test Empire",
            player=self.player,
            race=self.race,
            game=self.game
        )
        
        # Create empty empire for testing
        self.empty_empire = Empire.objects.create(
            name="Empty Empire",
            player=self.player,
            race=self.race,
            game=self.game
        )
        
        # Create test star system
        self.star = Star.objects.create(star_type="yellow")
        self.system = System.objects.create(
            x=1,
            y=1,
            star=self.star,
            game=self.game
        )
        
        # Create test planets with different production values
        self.planet1 = Planet.objects.create(
            system=self.system,
            empire=self.empire,
            orbit=1,  # First orbit
            mineral_production=Decimal('10'),
            organic_production=Decimal('20'),
            radioactive_production=Decimal('30'),
            exotic_production=Decimal('40'),
            mineral_storage_capacity=Decimal('100'),
            organic_storage_capacity=Decimal('100'),
            radioactive_storage_capacity=Decimal('100'),
            exotic_storage_capacity=Decimal('100')
        )
        
        self.planet2 = Planet.objects.create(
            system=self.system,
            empire=self.empire,
            orbit=2,  # Second orbit
            mineral_production=Decimal('15'),
            organic_production=Decimal('25'),
            radioactive_production=Decimal('35'),
            exotic_production=Decimal('45'),
            mineral_storage_capacity=Decimal('100'),
            organic_storage_capacity=Decimal('100'),
            radioactive_storage_capacity=Decimal('100'),
            exotic_storage_capacity=Decimal('100')
        )
        
        # Create test asteroid belt
        self.belt = AsteroidBelt.objects.create(
            system=self.system,
            empire=self.empire,
            orbit=3,  # Third orbit
            mineral_production=Decimal('5'),
            organic_production=Decimal('10'),
            radioactive_production=Decimal('15'),
            exotic_production=Decimal('20')
        )

    def test_process_turn_advances_counter(self):
        """Verify that processing a turn correctly advances the turn counter.
        
        Tests that:
        1. The turn counter is incremented
        2. The change is persisted to the database
        """
        # Process turn
        game = process(self.game)
        
        # Verify turn was advanced
        self.assertEqual(game.turn, 1)
        
        # Verify changes were saved to database
        self.game.refresh_from_db()
        self.assertEqual(self.game.turn, 1)

    def test_process_turn_returns_game(self):
        """Verify that process() returns the correct game instance.
        
        Tests that:
        1. The returned object is a Game instance
        2. The returned game is the same as the input game
        """
        # Process turn
        game = process(self.game)
        
        # Verify returned object is a Game instance
        self.assertIsInstance(game, Game)
        
        # Verify it's the same game instance
        self.assertEqual(game.id, self.game.id)

    def test_process_turn_multiple_times(self):
        """Verify that multiple turns can be processed correctly.
        
        Tests that:
        1. Turn counter advances correctly for multiple turns
        2. Database state is maintained correctly between turns
        """
        # Process multiple turns
        for expected_turn in range(1, 4):
            game = process(self.game)
            self.assertEqual(game.turn, expected_turn)
            
            # Verify database state
            self.game.refresh_from_db()
            self.assertEqual(self.game.turn, expected_turn)

    def test_calculate_resource_production(self):
        """Test resource production calculation."""
        mineral, organic, radioactive, exotic = calculate_resource_production(self.empire)
        
        # Check planet production
        self.assertEqual(mineral, Decimal('30'))  # 10 + 15 + 5
        self.assertEqual(organic, Decimal('55'))  # 20 + 25 + 10
        self.assertEqual(radioactive, Decimal('80'))  # 30 + 35 + 15
        self.assertEqual(exotic, Decimal('105'))  # 40 + 45 + 20
    
    def test_calculate_resource_production_no_bodies(self):
        """Test resource production calculation with no planets or belts."""
        mineral, organic, radioactive, exotic = calculate_resource_production(self.empty_empire)
        
        self.assertEqual(mineral, Decimal('0'))
        self.assertEqual(organic, Decimal('0'))
        self.assertEqual(radioactive, Decimal('0'))
        self.assertEqual(exotic, Decimal('0'))
    
    def test_update_empire_resources(self):
        """Test updating empire resources with production."""
        # Set initial storage values
        self.empire.mineral_storage = Decimal('50')
        self.empire.organic_storage = Decimal('50')
        self.empire.radioactive_storage = Decimal('50')
        self.empire.exotic_storage = Decimal('50')
        self.empire.save()
        
        # Update resources
        update_empire_resources(self.empire)
        
        # Refresh from database
        self.empire.refresh_from_db()
        
        # Check updated values
        self.assertEqual(self.empire.mineral_storage, Decimal('80'))  # 50 + 30
        self.assertEqual(self.empire.organic_storage, Decimal('105'))  # 50 + 55
        self.assertEqual(self.empire.radioactive_storage, Decimal('130'))  # 50 + 80
        self.assertEqual(self.empire.exotic_storage, Decimal('155'))  # 50 + 105
    
    def test_process_turn(self):
        """Test the main turn processing function."""
        # Set initial turn and storage values
        self.game.turn = 1
        self.game.save()
        
        self.empire.mineral_storage = Decimal('50')
        self.empire.organic_storage = Decimal('50')
        self.empire.radioactive_storage = Decimal('50')
        self.empire.exotic_storage = Decimal('50')
        self.empire.save()
        
        # Process turn
        updated_game = process(self.game)
        
        # Refresh empire from database
        self.empire.refresh_from_db()
        
        # Check turn was advanced
        self.assertEqual(updated_game.turn, 2)
        
        # Check resources were updated
        self.assertEqual(self.empire.mineral_storage, Decimal('80'))  # 50 + 30
        self.assertEqual(self.empire.organic_storage, Decimal('105'))  # 50 + 55
        self.assertEqual(self.empire.radioactive_storage, Decimal('130'))  # 50 + 80
        self.assertEqual(self.empire.exotic_storage, Decimal('155'))  # 50 + 105

    def tearDown(self):
        """Clean up test data by removing all game instances.
        
        Ensures the database is clean after each test run.
        """
        Game.objects.all().delete() 