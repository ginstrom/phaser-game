"""Tests for the turn processing functionality in the game.

This module contains test cases for the turn processing system, which handles
the advancement of game turns and associated state changes. The tests verify
that turns are properly advanced, game state is correctly updated, and changes
are persisted to the database.
"""

from django.test import TestCase
from play.models import Game
from play.turn import process

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

    def tearDown(self):
        """Clean up test data by removing all game instances.
        
        Ensures the database is clean after each test run.
        """
        Game.objects.all().delete() 