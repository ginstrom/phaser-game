from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from play.models import Player


class PlayerAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.player_list_url = reverse('player-list')
        self.human_player = Player.objects.create(player_type=Player.PlayerType.HUMAN)
        self.computer_player = Player.objects.create(player_type=Player.PlayerType.COMPUTER)

    def test_list_players(self):
        """Test retrieving a list of players"""
        response = self.client.get(self.player_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_player(self):
        """Test creating a new player"""
        data = {'player_type': Player.PlayerType.COMPUTER}
        response = self.client.post(self.player_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['player_type'], Player.PlayerType.COMPUTER)

    def test_create_player_invalid_type(self):
        """Test creating a player with invalid type"""
        data = {'player_type': 'invalid_type'}
        response = self.client.post(self.player_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_player(self):
        """Test retrieving a specific player"""
        url = reverse('player-detail', args=[self.human_player.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['player_type'], Player.PlayerType.HUMAN)

    def test_update_player(self):
        """Test updating a player"""
        url = reverse('player-detail', args=[self.human_player.id])
        data = {'player_type': Player.PlayerType.COMPUTER}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['player_type'], Player.PlayerType.COMPUTER)

    def test_delete_player(self):
        """Test deleting a player"""
        url = reverse('player-detail', args=[self.human_player.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.count(), 1)

    def tearDown(self):
        """Clean up test data"""
        Player.objects.all().delete()
