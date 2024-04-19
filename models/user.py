#!/usr/bin/python3
"""Module for user."""

from models.base_model import BaseModel


class User(BaseModel):
    """Class for user."""

    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
