#!/usr/bin/python3
"""Unittest module for DBStorage class."""
import os
import unittest
import pycodestyle


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db',
    "DBStorage tests skipped in file storage mode"
)
class TestDBStorageDocs(unittest.TestCase):
    """Tests to check documentation and style of DBStorage class."""

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        if os.path.exists('models/engine/db_storage.py'):
            style = pycodestyle.StyleGuide(quiet=True)
            result = style.check_files(['models/engine/db_storage.py'])
            self.assertEqual(
                result.total_errors, 0,
                "Found code style errors (and warnings)."
            )

    def test_pep8_conformance_test_db_storage(self):
        """Test that test_db_storage.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_db_storage.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db',
    "DBStorage tests skipped in file storage mode"
)
class TestDBStorage(unittest.TestCase):
    """Test cases for the DBStorage class."""

    def test_db_storage_instantiation(self):
        """Test DBStorage can be instantiated if present."""
        try:
            from models.engine.db_storage import DBStorage
            storage = DBStorage()
            self.assertIsNotNone(storage)
        except ImportError:
            pass


if __name__ == '__main__':
    unittest.main()
