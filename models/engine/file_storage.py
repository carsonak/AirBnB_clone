#!/usr/bin/python3
"""Module for file_storage."""

from contextlib import suppress
import json
import os
import typing

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Class for FileStorage."""

    __file_path: str = "saved_objects.json"
    __objects: typing.Dict[str, BaseModel] = dict()

    def all(self) -> typing.Dict[str, BaseModel]:
        """Return a dictionary of all objects."""
        return self.__objects

    def new(self, obj) -> None:
        """Add a new object to __objects."""
        obj_key: str = ".".join([obj.__class__.__name__, obj.id])
        self.__objects[obj_key] = obj

    def save(self) -> None:
        """Serialise all objects in __objects to a json file."""
        json_dict: typing.Dict[str, typing.Dict[str, str]] = {}
        for key, obj in self.__objects.items():
            json_dict[key] = obj.to_dict()

        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(json_dict, file, indent="    ")

    def reload(self) -> None:
        """Deserialize contents of a json file into __objects."""
        loaded_objs: typing.Dict[str, dict] = dict()
        with suppress(FileNotFoundError):
            if os.stat(self.__file_path).st_size > 0:
                with open(self.__file_path, "r", encoding="utf-8") as file:
                    loaded_objs = json.load(file)

        for key, obj_dict in loaded_objs.items():
            # Pulling the class from the global NameSpace dictionary
            self.__objects[key] = globals()[obj_dict["__class__"]](**obj_dict)
