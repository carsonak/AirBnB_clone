#!/usr/bin/python3
"""Module for test_city."""

from datetime import datetime
import unittest

import models
from models.city import City


class TestCity(unittest.TestCase):
    """Tests for City."""

    def tearDown(self) -> None:
        """Delete created instances."""
        models.storage._FileStorage__objects.clear()  # type: ignore

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        u: City = City()

        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)
        self.assertEqual(u.created_at, u.updated_at)
        self.assertIsInstance(u.state_id, str)
        self.assertIsInstance(u.name, str)
