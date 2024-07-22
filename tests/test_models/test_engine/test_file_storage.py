#!/usr/bin/env python3
"""Module for test_file_storage."""

import json
import typing
import unittest
from unittest import mock

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


class TestFileStorage(unittest.TestCase):
    """Tests for FileStorage."""

    def tearDown(self) -> None:
        """Delete created instances."""
        del self.storage
        del self.json_file_contents
        del self.objects_dict

    def test_instanceAttributes(self) -> None:  # noqa: N802
        """Check that the instance has the required attributes."""
        self.assertIsInstance(
            self.storage._FileStorage__file_path,  # type: ignore
            str)
        self.assertEqual(
            self.storage._FileStorage__file_path.endswith(  # type: ignore
                ".json"),
            True)
        self.assertIsInstance(
            self.storage._FileStorage__objects,  # type: ignore
            dict)

    def test_allEmpty(self) -> None:  # noqa: N802
        """Test the all method with empty __objects."""
        self.assertEqual(self.storage.all(), {})

    def test_allNotEmpty(self) -> None:  # noqa: N802
        """Test the all method with a non-empty __objects."""
        self.storage._FileStorage__objects = self.objects_dict  # type: ignore
        self.assertEqual(self.storage.all(), self.objects_dict)

    def test_new(self) -> None:
        """Test the method new."""
        for key, obj in self.objects_dict.items():
            with self.subTest(key=key, obj=obj):
                self.storage.new(obj)
                self.assertIn(
                    key,
                    self.storage._FileStorage__objects)  # type: ignore
                self.assertIsInstance(
                    self.storage._FileStorage__objects[key],  # type: ignore
                    type(obj))

        self.assertEqual(self.storage._FileStorage__objects,  # type: ignore
                         self.objects_dict)

    def test_saveEmpty(self) -> None:  # noqa: N802
        """Test the save method when __objects is empty."""
        with mock.patch("models.engine.file_storage.open",
                        new=mock.mock_open()) as fake_file:
            self.storage.save()
            fake_file.assert_called_once_with(
                self.storage._FileStorage__file_path,  # type: ignore
                "w", encoding="utf-8")
            fake_file().write.assert_called()

    def setUp(self) -> None:
        """Setup some data for testing."""
        storage._FileStorage__objects = {}  # type: ignore
        self.storage: FileStorage = FileStorage()
        self.json_file_contents: str = json.dumps({
            "User.368bf4c9-d31d-488f-a0df-82956df65d87": {
                "id": "368bf4c9-d31d-488f-a0df-82956df65d87",
                "created_at": "2024-04-20T22:54:27.010738",
                "updated_at": "2024-04-20T22:56:10.710577",
                "first_name": "Damian",
                "last_name": "Sal",
                "__class__": "User"
            },
            "Place.c4663bbb-0918-4c0a-9f28-1aba33ce53ff": {
                "id": "c4663bbb-0918-4c0a-9f28-1aba33ce53ff",
                "created_at": "2024-04-20T22:55:15.088887",
                "updated_at": "2024-04-21T12:46:27.944296",
                "amenity_ids": [
                    "60af1e59-4fde-4b8c-89e8-bd4bd4e4ee8e",
                    "a268f1ab-1bd2-450c-81a9-6df87dbe65af"
                ],
                "longitude": 44.789,
                "latitude": -52.08,
                "city_id": "0ad1a6d2-a47b-4728-8746-02854b9916d4",
                "user_id": "368bf4c9-d31d-488f-a0df-82956df65d87",
                "name": "Boshvle",
                "price_by_night": 170,
                "__class__": "Place"
            },
            "BaseModel.77503503-4e67-4d6a-833e-6b16127a4570": {
                "id": "77503503-4e67-4d6a-833e-6b16127a4570",
                "created_at": "2024-04-20T22:55:25.273094",
                "updated_at": "2024-04-20T22:55:25.273113",
                "__class__": "BaseModel"
            },
            "Amenity.a268f1ab-1bd2-450c-81a9-6df87dbe65af": {
                "id": "a268f1ab-1bd2-450c-81a9-6df87dbe65af",
                "created_at": "2024-04-21T11:46:44.343338",
                "updated_at": "2024-04-21T12:05:52.911487",
                "name": "pool",
                "__class__": "Amenity"
            },
            "City.0ad1a6d2-a47b-4728-8746-02854b9916d4": {
                "id": "0ad1a6d2-a47b-4728-8746-02854b9916d4",
                "created_at": "2024-04-21T11:48:40.438292",
                "updated_at": "2024-04-21T12:17:08.986327",
                "state_id": "25d6c4f3-a8d3-43aa-bc42-76397f19dbdd",
                "name": "Kaokao",
                "__class__": "City"
            },
            "State.25d6c4f3-a8d3-43aa-bc42-76397f19dbdd": {
                "id": "25d6c4f3-a8d3-43aa-bc42-76397f19dbdd",
                "created_at": "2024-04-21T11:53:05.705036",
                "updated_at": "2024-04-21T12:19:34.259996",
                "name": "Babon",
                "__class__": "State"
            },
            "Review.46ef68d5-bb2f-44e5-ab14-9c8d365cbcb8": {
                "id": "46ef68d5-bb2f-44e5-ab14-9c8d365cbcb8",
                "created_at": "2024-04-21T11:53:19.024671",
                "updated_at": "2024-04-21T12:39:22.883356",
                "place_id": "c4663bbb-0918-4c0a-9f28-1aba33ce53ff",
                "user_id": "368bf4c9-d31d-488f-a0df-82956df65d87",
                "text": "Wonderful!",
                "__class__": "Review"
            },
            "Amenity.60af1e59-4fde-4b8c-89e8-bd4bd4e4ee8e": {
                "id": "60af1e59-4fde-4b8c-89e8-bd4bd4e4ee8e",
                "created_at": "2024-04-21T12:40:38.299545",
                "updated_at": "2024-04-21T12:41:17.945658",
                "name": "balcony",
                "__class__": "Amenity"
            }
        }, indent="\t")

        self.objects_dict: typing.Dict[str, BaseModel] = {
            "User.368bf4c9-d31d-488f-a0df-82956df65d87": User(
                id="368bf4c9-d31d-488f-a0df-82956df65d87",
                created_at="2024-04-20T22:54:27.010738",
                updated_at="2024-04-20T22:56:10.710577",
                first_name="Damian",
                last_name="Sal",
                __class__="User"
            ),
            "Place.c4663bbb-0918-4c0a-9f28-1aba33ce53ff": Place(
                id="c4663bbb-0918-4c0a-9f28-1aba33ce53ff",
                created_at="2024-04-20T22:55:15.088887",
                updated_at="2024-04-21T12:46:27.944296",
                amenity_ids=[
                    "60af1e59-4fde-4b8c-89e8-bd4bd4e4ee8e",
                    "a268f1ab-1bd2-450c-81a9-6df87dbe65af"
                ],
                longitude=44.789,
                latitude=-52.08,
                city_id="0ad1a6d2-a47b-4728-8746-02854b9916d4",
                user_id="368bf4c9-d31d-488f-a0df-82956df65d87",
                name="Boshvle",
                price_by_night=170,
                __class__="Place"
            ),
            "BaseModel.77503503-4e67-4d6a-833e-6b16127a4570": BaseModel(
                id="77503503-4e67-4d6a-833e-6b16127a4570",
                created_at="2024-04-20T22:55:25.273094",
                updated_at="2024-04-20T22:55:25.273113",
                __class__="BaseModel"
            ),
            "Amenity.a268f1ab-1bd2-450c-81a9-6df87dbe65af": Amenity(
                id="a268f1ab-1bd2-450c-81a9-6df87dbe65af",
                created_at="2024-04-21T11:46:44.343338",
                updated_at="2024-04-21T12:05:52.911487",
                name="pool",
                __class__="Amenity"
            ),
            "City.0ad1a6d2-a47b-4728-8746-02854b9916d4": City(
                id="0ad1a6d2-a47b-4728-8746-02854b9916d4",
                created_at="2024-04-21T11:48:40.438292",
                updated_at="2024-04-21T12:17:08.986327",
                state_id="25d6c4f3-a8d3-43aa-bc42-76397f19dbdd",
                name="Kaokao",
                __class__="City"
            ),
            "State.25d6c4f3-a8d3-43aa-bc42-76397f19dbdd": State(
                id="25d6c4f3-a8d3-43aa-bc42-76397f19dbdd",
                created_at="2024-04-21T11:53:05.705036",
                updated_at="2024-04-21T12:19:34.259996",
                name="Babon",
                __class__="State"
            ),
            "Review.46ef68d5-bb2f-44e5-ab14-9c8d365cbcb8": Review(
                id="46ef68d5-bb2f-44e5-ab14-9c8d365cbcb8",
                created_at="2024-04-21T11:53:19.024671",
                updated_at="2024-04-21T12:39:22.883356",
                place_id="c4663bbb-0918-4c0a-9f28-1aba33ce53ff",
                user_id="368bf4c9-d31d-488f-a0df-82956df65d87",
                text="Wonderful!",
                __class__="Review"
            ),
            "Amenity.60af1e59-4fde-4b8c-89e8-bd4bd4e4ee8e": Amenity(
                id="60af1e59-4fde-4b8c-89e8-bd4bd4e4ee8e",
                created_at="2024-04-21T12:40:38.299545",
                updated_at="2024-04-21T12:41:17.945658",
                name="balcony",
                __class__="Amenity"
            )
        }


if __name__ == "__main__":
    unittest.main()
