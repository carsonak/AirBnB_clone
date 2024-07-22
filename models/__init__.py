#!/usr/bin/python3
"""Module for __init__."""

from models.engine.file_storage import FileStorage


storage: FileStorage = FileStorage()
storage.reload()
