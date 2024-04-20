#!/usr/bin/python3
"""Module for base_model."""

import uuid
import models
from datetime import datetime


class BaseModel:
    """Base model class."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialise some attributes."""
        if kwargs:
            kwargs.pop("__class__", None)
            kwargs["created_at"] = datetime.fromisoformat(kwargs["created_at"])
            kwargs["updated_at"] = datetime.fromisoformat(kwargs["updated_at"])
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self.id: str = str(uuid.uuid4())
            self.created_at: datetime = datetime.now()
            self.updated_at: datetime = self.created_at
            models.storage.new(self)

    def __str__(self) -> str:
        """Print details about the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self) -> None:
        """Update updated_at to current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self) -> dict[str, str]:
        """Return the __dict__ attribute of an instance."""
        ins_dict: dict = dict(self.__dict__)
        ins_dict["__class__"] = self.__class__.__name__
        ins_dict["created_at"] = self.created_at.isoformat()
        ins_dict["updated_at"] = self.updated_at.isoformat()

        return ins_dict
