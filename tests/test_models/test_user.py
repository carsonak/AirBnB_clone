#!/usr/bin/python3
"""Module for test_user."""

from datetime import datetime
import unittest

from models.user import User


class TestUser(unittest.TestCase):
    """Tests for User."""

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        u: User = User()

        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)
        self.assertEqual(u.created_at, u.updated_at)
        self.assertIsInstance(u.email, str)
        self.assertIsInstance(u.password, str)
        self.assertIsInstance(u.first_name, str)
        self.assertIsInstance(u.last_name, str)
