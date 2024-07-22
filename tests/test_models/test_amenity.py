#!/usr/bin/python3
"""Module for test_amenity."""

from datetime import datetime
import unittest

from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Tests for Amenity."""

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        u: Amenity = Amenity()

        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)
        self.assertEqual(u.created_at, u.updated_at)
        self.assertIsInstance(u.name, str)
