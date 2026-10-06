#!/usr/bin/python3
"""Unittest module for City class."""
import inspect
import unittest
import pycodestyle
import models
from models.base_model import BaseModel
from models.city import City


class TestCityDocs(unittest.TestCase):
    """Tests to check documentation and style of City class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.city_funcs = inspect.getmembers(
            City, inspect.isfunction
        )

    def test_pep8_conformance_city(self):
        """Test that models/city.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/city.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_city(self):
        """Test that tests/test_models/test_city.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_city.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_city_module_docstring(self):
        """Test for the city.py module docstring."""
        self.assertIsNotNone(
            models.city.__doc__,
            "city.py needs a docstring"
        )
        self.assertTrue(
            len(models.city.__doc__) >= 1,
            "city.py needs a docstring"
        )

    def test_city_class_docstring(self):
        """Test for the City class docstring."""
        self.assertIsNotNone(
            City.__doc__,
            "City class needs a docstring"
        )
        self.assertTrue(
            len(City.__doc__) >= 1,
            "City class needs a docstring"
        )


class TestCity(unittest.TestCase):
    """Test cases for the City class."""

    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel."""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_state_id_attr(self):
        """Test City has attr state_id, and it's an empty string."""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        self.assertEqual(city.state_id, "")

    def test_name_attr(self):
        """Test City has attr name, and it's an empty string."""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        self.assertEqual(city.name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attributes."""
        c = City()
        c.name = "San Francisco"
        c.state_id = "CA"
        new_d = c.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(new_d["name"], "San Francisco")
        self.assertEqual(new_d["state_id"], "CA")
        self.assertIsInstance(new_d["created_at"], str)
        self.assertIsInstance(new_d["updated_at"], str)

    def test_str(self):
        """Test that the str method has the correct output."""
        city = City()
        string = str(city)
        self.assertIn("[City]", string)
        self.assertIn(city.id, string)


if __name__ == '__main__':
    unittest.main()
