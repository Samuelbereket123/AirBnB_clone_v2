#!/usr/bin/python3
"""Unittest module for FileStorage class."""
import inspect
import json
import os
import unittest
import pycodestyle
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check documentation and style of FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.fs_funcs = inspect.getmembers(
            FileStorage, inspect.isfunction
        )

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_file_storage(self):
        """Test that tests/.../test_file_storage.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_file_storage.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring."""
        self.assertIsNotNone(
            models.engine.file_storage.__doc__,
            "file_storage.py needs a docstring"
        )
        self.assertTrue(
            len(models.engine.file_storage.__doc__) >= 1,
            "file_storage.py needs a docstring"
        )

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring."""
        self.assertIsNotNone(
            FileStorage.__doc__,
            "FileStorage class needs a docstring"
        )
        self.assertTrue(
            len(FileStorage.__doc__) >= 1,
            "FileStorage class needs a docstring"
        )

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods."""
        for func in self.fs_funcs:
            self.assertIsNotNone(
                func[1].__doc__,
                "{:s} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0])
            )


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db',
    "FileStorage tests skipped in db storage mode"
)
class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class."""

    def setUp(self):
        """Set up test environment."""
        self.storage = FileStorage()
        self.reset_file()

    def tearDown(self):
        """Clean up test environment."""
        self.reset_file()

    def reset_file(self):
        """Remove file.json if exists and reset objects."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dict(self):
        """Test that all returns a dictionary."""
        self.assertEqual(type(self.storage.all()), dict)

    def test_new(self):
        """Test that new adds an object to the __objects dictionary."""
        bm = BaseModel()
        self.storage.new(bm)
        key = "BaseModel." + bm.id
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], bm)

    def test_all_with_cls(self):
        """Test all method with class filter."""
        s = State()
        s.name = "California"
        c = City()
        c.name = "San Francisco"
        self.storage.new(s)
        self.storage.new(c)
        state_objs = self.storage.all(State)
        self.assertIn("State." + s.id, state_objs)
        self.assertNotIn("City." + c.id, state_objs)

    def test_save(self):
        """Test that save properly saves objects to file.json."""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.assertTrue(os.path.exists("file.json"))
        with open("file.json", "r") as f:
            data = json.load(f)
        key = "BaseModel." + bm.id
        self.assertIn(key, data)
        self.assertEqual(data[key]["id"], bm.id)

    def test_reload(self):
        """Test that reload properly loads objects from file.json."""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        FileStorage._FileStorage__objects = {}
        self.storage.reload()
        key = "BaseModel." + bm.id
        self.assertIn(key, self.storage.all())

    def test_reload_no_file(self):
        """Test that reload does not fail when file.json doesn't exist."""
        try:
            self.storage.reload()
        except Exception as e:
            self.fail("reload() raised exception: {}".format(e))

    def test_delete(self):
        """Test delete method removes object from storage."""
        bm = BaseModel()
        self.storage.new(bm)
        key = "BaseModel." + bm.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(bm)
        self.assertNotIn(key, self.storage.all())

    def test_close(self):
        """Test close method calls reload."""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        FileStorage._FileStorage__objects = {}
        self.storage.close()
        key = "BaseModel." + bm.id
        self.assertIn(key, self.storage.all())


if __name__ == '__main__':
    unittest.main()
