from django.test import TestCase
from play.models import Game
from play.turn import process

class TurnProcessingTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.game = Game.objects.create(turn=0)

    def test_process_turn_advances_counter(self):
        """Test that process() advances the turn counter"""
        # Process turn
        game = process(self.game)
        
        # Verify turn was advanced
        self.assertEqual(game.turn, 1)
        
        # Verify changes were saved to database
        self.game.refresh_from_db()
        self.assertEqual(self.game.turn, 1)

    def test_process_turn_returns_game(self):
        """Test that process() returns the game instance"""
        # Process turn
        game = process(self.game)
        
        # Verify returned object is a Game instance
        self.assertIsInstance(game, Game)
        
        # Verify it's the same game instance
        self.assertEqual(game.id, self.game.id)

    def test_process_turn_multiple_times(self):
        """Test processing multiple turns"""
        # Process multiple turns
        for expected_turn in range(1, 4):
            game = process(self.game)
            self.assertEqual(game.turn, expected_turn)
            
            # Verify database state
            self.game.refresh_from_db()
            self.assertEqual(self.game.turn, expected_turn)

    def tearDown(self):
        """Clean up test data"""
        Game.objects.all().delete() 