#!/usr/bin/python3
"""Module for test_amenity."""

from datetime import datetime
import unittest

import models
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Tests for Amenity."""

    def tearDown(self) -> None:
        """Delete created instances."""
        models.storage._FileStorage__objects.clear()  # type: ignore

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        am: Amenity = Amenity()

        self.assertIsInstance(am.id, str)
        self.assertIsInstance(am.created_at, datetime)
        self.assertEqual(am.created_at, am.updated_at)
        self.assertIsInstance(am.name, str)
