#!/usr/bin/python3
"""Module for test_base_model."""

from datetime import datetime
import typing
import unittest
from unittest import mock

from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel."""

    def setUp(self) -> None:
        """Create some instances."""
        storage._FileStorage__objects = {}  # type: ignore
        self.new: BaseModel = BaseModel()
        self.old_dict: typing.Dict[str, str] = \
            {"id": "c9831ae2-6cba-42fc-9634-acf1c36631e1",
             "created_at": "2024-04-20T10:00:40.789191",
             "updated_at": "2024-04-20T10:00:40.789222",
             "__class__": "User"}
        #  "name": ("Doe", "John"),  # type: ignore
        #  "age": 45}  # type: ignore
        self.old: BaseModel = BaseModel(**self.old_dict)
        self.old_dict["__class__"] = "BaseModel"

    def tearDown(self) -> None:
        """Teardown."""
        del self.new
        del self.old
        del self.old_dict

    def test_new_instance_attributes(self) -> None:
        """Test attributes of a new instance."""
        self.assertIsInstance(self.new.id, str)
        self.assertIsInstance(self.new.created_at, datetime)
        self.assertEqual(self.new.created_at, self.new.updated_at)

    def test_old_instance_attributes(self) -> None:
        """Test attributes of an old instance."""
        self.assertEqual(self.old.id, self.old_dict["id"])
        self.assertFalse(hasattr(self.old, "name"))
        self.assertFalse(hasattr(self.old, "age"))
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
'updated_at': datetime.datetime(2024, 4, 20, 10, 0, 40, 789222)}"
# 'name': ('Doe', 'John'), 'age': 45}"

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
            fake_open.assert_called_once_with("saved_objects.json",
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
        instance_dict: typing.Dict[str, str] = self.old.to_dict()
        self.assertEqual(instance_dict, self.old_dict)


if __name__ == "__main__":
    unittest.main()
