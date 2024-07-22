#!/usr/bin/env python3
"""Module for amenity."""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """Class for Amenity."""

    name: str = ""
