#!/usr/bin/python3
"""Module for test_base_model."""

from datetime import datetime
import unittest
from unittest import mock
from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel."""

    def setUp(self):
        """Create some instances."""
        storage._FileStorage__objects = {}
        self.new = BaseModel()
        self.old_dict = {
            "id": "c9831ae2-6cba-42fc-9634-acf1c36631e1",
            "created_at": "2024-04-20T10:00:40.789191",
            "updated_at": "2024-04-20T10:00:40.789222",
            "__class__": "User"
        }
        self.old = BaseModel(**self.old_dict)
        self.old_dict['__class__'] = 'BaseModel'

    def tearDown(self):
        """Teardown."""
        del self.new
        del self.old
        del self.old_dict

    def test_new_instance_attributes(self):
        """Test attributes of a new instance."""
        self.assertIsInstance(self.new.id, str)
        self.assertEqual(len(self.new.id.split('-')), 5)
        self.assertIsInstance(self.new.created_at, datetime)
        self.assertEqual(self.new.created_at, self.new.updated_at)

    def test_old_instance_attributes(self):
        """Test attributes of an old instance."""
        self.assertEqual(self.old.id, self.old_dict['id'])
        self.assertEqual(hasattr(self.old, 'name'), False)
        self.assertEqual(hasattr(self.old, 'age'), False)
        self.assertEqual(self.old.created_at, datetime.fromisoformat(
            self.old_dict['created_at']))
        self.assertEqual(self.old.updated_at, datetime.fromisoformat(
            self.old_dict['updated_at']))
        self.assertEqual(self.old.__class__.__name__,
                         self.old_dict['__class__'])

    def test_str(self):
        """Test the __str__ method."""
        excepted_output = (
            "[BaseModel] (c9831ae2-6cba-42fc-9634-acf1c36631e1) "
            "{'id': 'c9831ae2-6cba-42fc-9634-acf1c36631e1', "
            "'created_at': datetime.datetime(2024, 4, 20, 10, 0, 40, 789191), "
            "'updated_at': datetime.datetime(2024, 4, 20, 10, 0, 40, 789222)}"
        )
        self.assertEqual(str(self.old), excepted_output)

    def test_save(self):
        """Test the save method."""
        before = BaseModel(
            id=self.new.id, created_at=self.new.created_at.isoformat(),
            updated_at=self.new.updated_at.isoformat()
        )
        self.new.name = 'Lolo'
        self.new.number = float('inf')
        with mock.patch(
            'models.engine.file_storage.open', new_callable=mock.mock_open
        ) as fake_open:
            self.new.save()
            fake_open.assert_called_once_with(
                'saved_objects.json', 'w', encoding='utf-8')
            fake_open().write.assert_called()

        after = self.new
        self.assertNotEqual(before, after)
        self.assertLess(before.updated_at, after.updated_at)
        self.assertEqual(before.created_at, after.created_at)
        self.assertEqual(before.id, after.id)
        with self.assertRaises(
                AttributeError, msg="Should not have attribute 'name'."):
            print(before.name)

        with self.assertRaises(
                AttributeError, msg="Should not have attribute 'number'."):
            print(before.number)

        self.assertEqual(after.name, 'Lolo')
        self.assertEqual(after.number, float('inf'))

    def test_todict(self):
        """Test the to_dict method."""
        instance_dict = self.old.to_dict()
        self.assertEqual(instance_dict, self.old_dict)


if __name__ == '__main__':
    unittest.main()
