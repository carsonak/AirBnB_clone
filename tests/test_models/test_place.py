#!/usr/bin/python3
"""Module for test_place."""

from datetime import datetime
import unittest

from models.place import Place


class TestPlace(unittest.TestCase):
    """Tests for Place."""

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        u: Place = Place()

        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)
        self.assertEqual(u.created_at, u.updated_at)
        self.assertIsInstance(u.city_id, str)
        self.assertIsInstance(u.user_id, str)
        self.assertIsInstance(u.name, str)
        self.assertIsInstance(u.description, str)
        self.assertIsInstance(u.number_rooms, int)
        self.assertIsInstance(u.number_bathrooms, int)
        self.assertIsInstance(u.max_guest, int)
        self.assertIsInstance(u.price_by_night, int)
        self.assertIsInstance(u.latitude, float)
        self.assertIsInstance(u.longitude, float)
        self.assertIsInstance(u.amenity_ids, list)
