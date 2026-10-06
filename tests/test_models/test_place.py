#!/usr/bin/python3
"""Unittest module for Place class."""
import inspect
import unittest
import pycodestyle
import models
from models.base_model import BaseModel
from models.place import Place


class TestPlaceDocs(unittest.TestCase):
    """Tests to check documentation and style of Place class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.place_funcs = inspect.getmembers(
            Place, inspect.isfunction
        )

    def test_pep8_conformance_place(self):
        """Test that models/place.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_place(self):
        """Test that tests/test_models/test_place.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_place.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_place_module_docstring(self):
        """Test for the place.py module docstring."""
        self.assertIsNotNone(
            models.place.__doc__,
            "place.py needs a docstring"
        )
        self.assertTrue(
            len(models.place.__doc__) >= 1,
            "place.py needs a docstring"
        )

    def test_place_class_docstring(self):
        """Test for the Place class docstring."""
        self.assertIsNotNone(
            Place.__doc__,
            "Place class needs a docstring"
        )
        self.assertTrue(
            len(Place.__doc__) >= 1,
            "Place class needs a docstring"
        )


class TestPlace(unittest.TestCase):
    """Test cases for the Place class."""

    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel."""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

    def test_city_id_attr(self):
        """Test Place has attr city_id, and it's an empty string."""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        self.assertEqual(place.city_id, "")

    def test_user_id_attr(self):
        """Test Place has attr user_id, and it's an empty string."""
        place = Place()
        self.assertTrue(hasattr(place, "user_id"))
        self.assertEqual(place.user_id, "")

    def test_name_attr(self):
        """Test Place has attr name, and it's an empty string."""
        place = Place()
        self.assertTrue(hasattr(place, "name"))
        self.assertEqual(place.name, "")

    def test_description_attr(self):
        """Test Place has attr description, and it's an empty string."""
        place = Place()
        self.assertTrue(hasattr(place, "description"))
        self.assertEqual(place.description, "")

    def test_number_rooms_attr(self):
        """Test Place has attr number_rooms, and it's 0."""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))
        self.assertEqual(type(place.number_rooms), int)
        self.assertEqual(place.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test Place has attr number_bathrooms, and it's 0."""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))
        self.assertEqual(type(place.number_bathrooms), int)
        self.assertEqual(place.number_bathrooms, 0)

    def test_max_guest_attr(self):
        """Test Place has attr max_guest, and it's 0."""
        place = Place()
        self.assertTrue(hasattr(place, "max_guest"))
        self.assertEqual(type(place.max_guest), int)
        self.assertEqual(place.max_guest, 0)

    def test_price_by_night_attr(self):
        """Test Place has attr price_by_night, and it's 0."""
        place = Place()
        self.assertTrue(hasattr(place, "price_by_night"))
        self.assertEqual(type(place.price_by_night), int)
        self.assertEqual(place.price_by_night, 0)

    def test_latitude_attr(self):
        """Test Place has attr latitude, and it's 0.0."""
        place = Place()
        self.assertTrue(hasattr(place, "latitude"))
        self.assertEqual(type(place.latitude), float)
        self.assertEqual(place.latitude, 0.0)

    def test_longitude_attr(self):
        """Test Place has attr longitude, and it's 0.0."""
        place = Place()
        self.assertTrue(hasattr(place, "longitude"))
        self.assertEqual(type(place.longitude), float)
        self.assertEqual(place.longitude, 0.0)

    def test_amenity_ids_attr(self):
        """Test Place has attr amenity_ids, and it's an empty list."""
        place = Place()
        self.assertTrue(hasattr(place, "amenity_ids"))
        self.assertEqual(type(place.amenity_ids), list)
        self.assertEqual(len(place.amenity_ids), 0)

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attributes."""
        p = Place()
        p.name = "Cozy Apartment"
        p.number_rooms = 2
        p.price_by_night = 100
        new_d = p.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(new_d["name"], "Cozy Apartment")
        self.assertEqual(new_d["number_rooms"], 2)
        self.assertEqual(new_d["price_by_night"], 100)
        self.assertIsInstance(new_d["created_at"], str)
        self.assertIsInstance(new_d["updated_at"], str)

    def test_str(self):
        """Test that the str method has the correct output."""
        place = Place()
        string = str(place)
        self.assertIn("[Place]", string)
        self.assertIn(place.id, string)


if __name__ == '__main__':
    unittest.main()
