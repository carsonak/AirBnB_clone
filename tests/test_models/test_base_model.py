#!/usr/bin/python3
"""Module for test_base_model."""

import models
import unittest
from models.base_model import BaseModel
from datetime import datetime
from unittest import mock


class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel."""

    def setUp(self) -> None:
        """Create some instances."""
        self.new: BaseModel = BaseModel()
        self.old_dict: dict[str, str] = \
            {"id": "c9831ae2-6cba-42fc-9634-acf1c36631e1",
             "created_at": "2024-04-20T10:00:40.789191",
             "updated_at": "2024-04-20T10:00:40.789222",
             "__class__": "User",
             "name": ("Doe", "John"),  # type: ignore
             "age": 45}  # type: ignore
        self.old: BaseModel = BaseModel(**self.old_dict)
        self.old_dict["__class__"] = "BaseModel"

    def tearDown(self) -> None:
        """Teardown."""
        return super().tearDown()

    def test_newInstanceAttributes(self) -> None:
        """Test attributes of a new instance."""
        self.assertEqual(type(self.new.id), str)
        self.assertEqual(len(self.new.id.split("-")), 5)
        self.assertEqual(type(self.new.created_at), datetime)
        self.assertEqual(self.new.created_at, self.new.updated_at)
        ins_key = ".".join(["BaseModel", self.new.id])
        self.assertEqual(
            models.storage._FileStorage__objects[ins_key],  # type: ignore
            self.new)

    def test_oldInstanceAttributes(self) -> None:
        """Test attributes of an old instance."""
        self.assertEqual(self.old.id, self.old_dict["id"])
        self.assertEqual(self.old.name, self.old_dict["name"])  # type: ignore
        self.assertEqual(self.old.age, self.old_dict["age"])  # type: ignore
        self.assertEqual(self.old.created_at, datetime.fromisoformat(
            self.old_dict["created_at"]))
        self.assertEqual(self.old.updated_at, datetime.fromisoformat(
            self.old_dict["updated_at"]))
        self.assertEqual(self.old.__class__.__name__,
                         self.old_dict["__class__"])

    def test_str(self) -> None:
        """Test the __str__ method."""
        excepted_output: str = "[BaseModel] \
(c9831ae2-6cba-42fc-9634-acf1c36631e1) \
{'id': 'c9831ae2-6cba-42fc-9634-acf1c36631e1', \
'created_at': datetime.datetime(2024, 4, 20, 10, 0, 40, 789191), \
'updated_at': datetime.datetime(2024, 4, 20, 10, 0, 40, 789222), \
'name': ('Doe', 'John'), 'age': 45}"

        self.assertEqual(str(self.old), excepted_output)

    def test_save(self) -> None:
        """Test the save method."""
        before: BaseModel = BaseModel(
            id=self.new.id, created_at=self.new.created_at.isoformat(),
            updated_at=self.new.updated_at.isoformat())

        self.new.name = "Lolo"  # type: ignore
        self.new.number = float("inf")  # type: ignore
        with mock.patch("models.engine.file_storage.open",
                        new_callable=mock.mock_open) as fake_open:
            self.new.save()
            fake_open.assert_called_once_with(
                models.storage._FileStorage__file_path,  # type: ignore
                "w", encoding="utf-8")
            fake_open().write.assert_called()

        after: BaseModel = self.new
        self.assertNotEqual(before, after)
        self.assertLess(before.updated_at, after.updated_at)
        self.assertEqual(before.created_at, after.created_at)
        self.assertEqual(before.id, after.id)
        with self.assertRaises(AttributeError,
                               msg="Should not have attribute 'name'."):
            print(before.name)  # type: ignore

        with self.assertRaises(AttributeError,
                               msg="Should not have attribute 'number'."):
            print(before.number)  # type: ignore

        self.assertEqual(after.name, "Lolo")  # type: ignore
        self.assertEqual(after.number, float("inf"))  # type: ignore

    def test_todict(self) -> None:
        """Test the to_dict method."""
        instance_dict: dict[str, str] = self.old.to_dict()
        self.assertEqual(instance_dict, self.old_dict)
