#!/usr/bin/env python3
"""Module for city."""

from models.base_model import BaseModel


class City(BaseModel):
    """Class for City."""

    state_id: str = ""
    name: str = ""
