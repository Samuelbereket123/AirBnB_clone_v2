#!/usr/bin/python3
"""Initializes the models package and creates a storage instance."""
import os
from models.engine.file_storage import FileStorage

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    try:
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
    except ImportError:
        storage = FileStorage()
else:
    storage = FileStorage()
storage.reload()
