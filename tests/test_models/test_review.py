#!/usr/bin/python3
"""Module for test_review."""

from datetime import datetime
import unittest

import models
from models.review import Review


class TestReview(unittest.TestCase):
    """Tests for Review."""

    def tearDown(self) -> None:
        """Delete created instances."""
        models.storage._FileStorage__objects.clear()  # type: ignore

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        u: Review = Review()

        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)
        self.assertEqual(u.created_at, u.updated_at)
        self.assertIsInstance(u.place_id, str)
        self.assertIsInstance(u.user_id, str)
        self.assertIsInstance(u.text, str)
