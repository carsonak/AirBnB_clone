#!/usr/bin/python3
"""Module for test_state."""

from datetime import datetime
import unittest

import models
from models.state import State


class TestState(unittest.TestCase):
    """Tests for State."""

    def tearDown(self) -> None:
        """Delete created instances."""
        models.storage._FileStorage__objects.clear()  # type: ignore

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        u: State = State()

        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)
        self.assertEqual(u.created_at, u.updated_at)
        self.assertIsInstance(u.name, str)
