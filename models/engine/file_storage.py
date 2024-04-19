#!/usr/bin/python3
"""Module for file_storage."""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class for FileStorage."""

    __file_path: str = "saved_objects.json"
    __objects: dict[str, BaseModel] = dict()

    def all(self) -> dict[str, BaseModel]:
        """Return a dictionary of all objects."""
        return self.__objects

    def new(self, obj) -> None:
        """Add a new object to __objects."""
        obj_key: str = ".".join([obj.__class__.__name__, obj.id])
        self.__objects[obj_key] = obj

    def save(self) -> None:
        """Serialise all objects in __objects to a json file."""
        json_dict: dict[str, dict[str, str]] = {key: obj.to_dict()
                                                for key, obj in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(json_dict, file)

    def reload(self) -> None:
        """Deserialise contents of a json file into __objects."""
        loaded_objs: dict[str, dict] = dict()
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                loaded_objs = json.load(file)
        except FileNotFoundError:
            pass

        for key, obj_dict in loaded_objs.items():
            # Pulling the class from the global NameSpace dictionary
            self.__objects[key] = globals()[obj_dict["__class__"]](obj_dict)
