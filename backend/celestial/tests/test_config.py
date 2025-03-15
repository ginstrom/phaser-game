"""
Test configuration for the celestial app.
"""
from django.test import TestCase
from django.db import connection


class DatabaseConfigTest(TestCase):
    def test_using_sqlite_memory(self):
        """Test that we're using SQLite in-memory database for tests"""
        self.assertEqual(connection.vendor, 'sqlite')
        self.assertTrue(connection.settings_dict['NAME'].startswith('file:memorydb_')) 