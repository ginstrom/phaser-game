from django.test import TestCase
from play.models import Player


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
