#!/usr/bin/python3
"""Module for user."""

from models.base_model import BaseModel


class User(BaseModel):
    """Class for user."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
