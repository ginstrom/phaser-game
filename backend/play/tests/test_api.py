from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from play.models import Player, Race, Empire, Game
from celestial.models import Planet, AsteroidBelt, System, Star


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


class RaceAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.race_data = {'name': 'Humans'}
        self.race = Race.objects.create(name='Vulcans')

    def test_create_race(self):
        """Test creating a new race via API"""
        url = reverse('race-list')
        response = self.client.post(url, self.race_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Race.objects.count(), 2)
        self.assertEqual(Race.objects.get(name='Humans').name, 'Humans')

    def test_list_races(self):
        """Test listing all races"""
        url = reverse('race-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Vulcans')

    def test_retrieve_race(self):
        """Test retrieving a specific race"""
        url = reverse('race-detail', args=[self.race.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vulcans')

    def test_update_race(self):
        """Test updating a race"""
        url = reverse('race-detail', args=[self.race.id])
        updated_data = {'name': 'Klingons'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Race.objects.get(id=self.race.id).name, 'Klingons')

    def test_delete_race(self):
        """Test deleting a race"""
        url = reverse('race-detail', args=[self.race.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Race.objects.count(), 0)

    def test_create_duplicate_race(self):
        """Test that creating a race with duplicate name fails"""
        url = reverse('race-list')
        response = self.client.post(url, {'name': 'Vulcans'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        """Clean up test data"""
        Race.objects.all().delete()


class EmpireAPITests(APITestCase):
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
        
        # Assign planets and asteroid belt to empire
        self.planet1.empire = self.empire
        self.planet1.save()
        self.planet2.empire = self.empire
        self.planet2.save()
        self.asteroid_belt.empire = self.empire
        self.asteroid_belt.save()
        
        # Set up API client
        self.client = APIClient()
        self.url = reverse('empire-list')

    def test_list_empires(self):
        """Test retrieving a list of empires"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Empire')

    def test_create_empire(self):
        """Test creating a new empire"""
        data = {
            'name': 'New Empire',
            'player_id': self.player.id,
            'race_id': self.race.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Empire.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Empire')

    def test_retrieve_empire(self):
        """Test retrieving a specific empire"""
        url = reverse('empire-detail', args=[self.empire.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Empire')
        self.assertEqual(response.data['player']['id'], self.player.id)
        self.assertEqual(response.data['race']['id'], self.race.id)
        
        # Check resource capacities
        self.assertEqual(response.data['resource_capacities']['mineral_capacity'], 400)
        self.assertEqual(response.data['resource_capacities']['organic_capacity'], 500)
        self.assertEqual(response.data['resource_capacities']['radioactive_capacity'], 600)
        self.assertEqual(response.data['resource_capacities']['exotic_capacity'], 700)

    def test_update_empire(self):
        """Test updating an empire"""
        url = reverse('empire-detail', args=[self.empire.id])
        data = {
            'name': 'Updated Empire',
            'player_id': self.player.id,
            'race_id': self.race.id,
            'mineral_storage': 100,
            'organic_storage': 200,
            'radioactive_storage': 300,
            'exotic_storage': 400
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Empire')
        self.assertEqual(response.data['mineral_storage'], 100)
        self.assertEqual(response.data['organic_storage'], 200)
        self.assertEqual(response.data['radioactive_storage'], 300)
        self.assertEqual(response.data['exotic_storage'], 400)

    def test_delete_empire(self):
        """Test deleting an empire"""
        url = reverse('empire-detail', args=[self.empire.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Empire.objects.count(), 0)

    def test_update_empire_planets(self):
        """Test updating empire's planets"""
        url = reverse('empire-detail', args=[self.empire.id])
        data = {
            'name': self.empire.name,
            'player_id': self.player.id,
            'race_id': self.race.id,
            'planet_ids': [self.planet1.id]  # Remove planet2
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['planets']), 1)
        self.assertEqual(response.data['planets'][0]['id'], self.planet1.id)
        
        # Check updated resource capacities
        self.assertEqual(response.data['resource_capacities']['mineral_capacity'], 100)
        self.assertEqual(response.data['resource_capacities']['organic_capacity'], 150)
        self.assertEqual(response.data['resource_capacities']['radioactive_capacity'], 200)
        self.assertEqual(response.data['resource_capacities']['exotic_capacity'], 250)

    def test_update_empire_asteroid_belts(self):
        """Test updating empire's asteroid belts"""
        url = reverse('empire-detail', args=[self.empire.id])
        data = {
            'name': self.empire.name,
            'player_id': self.player.id,
            'race_id': self.race.id,
            'asteroid_belt_ids': []  # Remove all asteroid belts
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['asteroid_belts']), 0)

    def test_get_empire_planets(self):
        """Test getting all planets belonging to an empire"""
        url = reverse('empire-planets', args=[self.empire.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify planet data
        planet_orbits = [planet['orbit'] for planet in response.data]
        self.assertIn(self.planet1.orbit, planet_orbits)
        self.assertIn(self.planet2.orbit, planet_orbits)

    def test_get_empire_planets_empty(self):
        """Test getting planets for an empire with no planets"""
        # Create a new empire with no planets
        empty_empire = Empire.objects.create(
            name="Empty Empire",
            player=self.player,
            race=self.race
        )
        
        url = reverse('empire-planets', args=[empty_empire.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_empire_asteroid_belts(self):
        """Test getting all asteroid belts belonging to an empire"""
        url = reverse('empire-asteroid-belts', args=[self.empire.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Verify asteroid belt data
        asteroid_belt = response.data[0]
        self.assertEqual(asteroid_belt['orbit'], self.asteroid_belt.orbit)
        self.assertEqual(asteroid_belt['mineral_production'], '50.00')
        self.assertEqual(asteroid_belt['organic_production'], '60.00')
        self.assertEqual(asteroid_belt['radioactive_production'], '70.00')
        self.assertEqual(asteroid_belt['exotic_production'], '80.00')

    def test_get_empire_asteroid_belts_empty(self):
        """Test getting asteroid belts for an empire with no asteroid belts"""
        # Create a new empire with no asteroid belts
        empty_empire = Empire.objects.create(
            name="Empty Empire",
            player=self.player,
            race=self.race
        )
        
        url = reverse('empire-asteroid-belts', args=[empty_empire.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_nonexistent_empire_resources(self):
        """Test getting resources for a nonexistent empire"""
        # Test planets endpoint
        url = reverse('empire-planets', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Test asteroid belts endpoint
        url = reverse('empire-asteroid-belts', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        """Clean up test data"""
        Empire.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
        System.objects.all().delete()  # This will cascade delete planets and asteroid belts
        Star.objects.all().delete()


class GameAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create players
        self.player1 = Player.objects.create(player_type=Player.PlayerType.HUMAN)
        self.player2 = Player.objects.create(player_type=Player.PlayerType.COMPUTER)
        
        # Create race
        self.race = Race.objects.create(name="Test Race")
        
        # Create game
        self.game = Game.objects.create(turn=0)
        
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
        
        # Create systems
        star1 = Star.objects.create(star_type=Star.StarType.YELLOW)
        star2 = Star.objects.create(star_type=Star.StarType.BLUE)
        
        self.system1 = System.objects.create(
            x=0, y=0,
            star=star1,
            game=self.game
        )
        self.system2 = System.objects.create(
            x=1, y=1,
            star=star2,
            game=self.game
        )

    def test_create_game(self):
        """Test creating a new game"""
        url = reverse('game-list')
        response = self.client.post(url, {})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 2)  # Including the one from setUp
        self.assertEqual(response.data['turn'], 0)

    def test_list_games(self):
        """Test listing all games"""
        url = reverse('game-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_game_detail(self):
        """Test getting details of a specific game"""
        url = reverse('game-detail', args=[self.game.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['turn'], 0)
        self.assertEqual(len(response.data['empires']), 2)
        self.assertEqual(len(response.data['systems']), 2)

    def test_get_game_systems(self):
        """Test getting all systems for a game"""
        url = reverse('game-systems', args=[self.game.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check first system
        system1 = response.data[0]
        self.assertEqual(system1['x'], 0)
        self.assertEqual(system1['y'], 0)
        self.assertEqual(system1['star']['star_type'], 'yellow')
        
        # Check second system
        system2 = response.data[1]
        self.assertEqual(system2['x'], 1)
        self.assertEqual(system2['y'], 1)
        self.assertEqual(system2['star']['star_type'], 'blue')

    def test_get_game_systems_empty(self):
        """Test getting systems for a game with no systems"""
        # Create a new game with no systems
        empty_game = Game.objects.create(turn=0)
        url = reverse('game-systems', args=[empty_game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_game_systems_nonexistent(self):
        """Test getting systems for a nonexistent game"""
        url = reverse('game-systems', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_game_empires(self):
        """Test getting empires for a game"""
        url = reverse('game-empires', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        empire_names = [empire['name'] for empire in response.data]
        self.assertIn(self.empire1.name, empire_names)
        self.assertIn(self.empire2.name, empire_names)

    def test_get_game_empires_empty(self):
        """Test getting empires for a game with no empires"""
        # Create a new game with no empires
        empty_game = Game.objects.create(turn=0)
        url = reverse('game-empires', args=[empty_game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_game_empires_nonexistent(self):
        """Test getting empires for a nonexistent game"""
        url = reverse('game-empires', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_end_turn(self):
        """Test ending a turn"""
        url = reverse('game-end-turn', args=[self.game.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['turn'], 1)
        
        # Verify turn was updated in database
        self.game.refresh_from_db()
        self.assertEqual(self.game.turn, 1)

    def test_delete_game(self):
        """Test deleting a game"""
        url = reverse('game-detail', args=[self.game.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Game.objects.count(), 0)

    def tearDown(self):
        """Clean up test data"""
        System.objects.all().delete()
        Star.objects.all().delete()
        Empire.objects.all().delete()
        Game.objects.all().delete()
        Player.objects.all().delete()
        Race.objects.all().delete()
