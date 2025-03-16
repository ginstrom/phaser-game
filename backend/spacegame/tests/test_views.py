from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spacegame/home.html')

    def test_home_page_content(self):
        """Test that the home page contains expected content"""
        response = self.client.get(reverse('home'))
        content = response.content.decode()
        
        # Check title and headings
        self.assertIn('<title>Space Conquest - 4X Strategy Game</title>', content)
        self.assertIn('<h1>Space Conquest</h1>', content)
        self.assertIn('<h2>About the Game</h2>', content)
        
        # Check game features are present
        self.assertIn('Explore mysterious star systems', content)
        self.assertIn('Expand your empire', content)
        self.assertIn('Exploit resources', content)
        self.assertIn('Engage in epic space battles', content)
        
        # Check API links are present
        self.assertIn('href="/api/docs/"', content)
        self.assertIn('href="/api/redoc/"', content)
        self.assertIn('href="/api/"', content) 