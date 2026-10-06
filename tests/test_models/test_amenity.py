#!/usr/bin/python3
"""Unittest module for Amenity class."""
import inspect
import unittest
import pycodestyle
import models
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenityDocs(unittest.TestCase):
    """Tests to check documentation and style of Amenity class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.amenity_funcs = inspect.getmembers(
            Amenity, inspect.isfunction
        )

    def test_pep8_conformance_amenity(self):
        """Test that models/amenity.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_amenity(self):
        """Test that tests/test_models/test_amenity.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_amenity.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_amenity_module_docstring(self):
        """Test for the amenity.py module docstring."""
        self.assertIsNotNone(
            models.amenity.__doc__,
            "amenity.py needs a docstring"
        )
        self.assertTrue(
            len(models.amenity.__doc__) >= 1,
            "amenity.py needs a docstring"
        )

    def test_amenity_class_docstring(self):
        """Test for the Amenity class docstring."""
        self.assertIsNotNone(
            Amenity.__doc__,
            "Amenity class needs a docstring"
        )
        self.assertTrue(
            len(Amenity.__doc__) >= 1,
            "Amenity class needs a docstring"
        )


class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity class."""

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel."""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_attr(self):
        """Test Amenity has attr name, and it's an empty string."""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        self.assertEqual(amenity.name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attributes."""
        a = Amenity()
        a.name = "Wifi"
        new_d = a.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertEqual(new_d["__class__"], "Amenity")
        self.assertEqual(new_d["name"], "Wifi")
        self.assertIsInstance(new_d["created_at"], str)
        self.assertIsInstance(new_d["updated_at"], str)

    def test_str(self):
        """Test that the str method has the correct output."""
        amenity = Amenity()
        string = str(amenity)
        self.assertIn("[Amenity]", string)
        self.assertIn(amenity.id, string)


if __name__ == '__main__':
    unittest.main()
