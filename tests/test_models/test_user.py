#!/usr/bin/python3
"""Unittest module for User class."""
import inspect
import unittest
import pycodestyle
import models
from models.base_model import BaseModel
from models.user import User


class TestUserDocs(unittest.TestCase):
    """Tests to check documentation and style of User class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.user_funcs = inspect.getmembers(
            User, inspect.isfunction
        )

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/user.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_models/test_user.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_user.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_user_module_docstring(self):
        """Test for the user.py module docstring."""
        self.assertIsNotNone(
            models.user.__doc__,
            "user.py needs a docstring"
        )
        self.assertTrue(
            len(models.user.__doc__) >= 1,
            "user.py needs a docstring"
        )

    def test_user_class_docstring(self):
        """Test for the User class docstring."""
        self.assertIsNotNone(
            User.__doc__,
            "User class needs a docstring"
        )
        self.assertTrue(
            len(User.__doc__) >= 1,
            "User class needs a docstring"
        )


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel."""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """Test User has attr email, and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertEqual(user.email, "")

    def test_password_attr(self):
        """Test User has attr password, and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "password"))
        self.assertEqual(user.password, "")

    def test_first_name_attr(self):
        """Test User has attr first_name, and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        self.assertEqual(user.first_name, "")

    def test_last_name_attr(self):
        """Test User has attr last_name, and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        self.assertEqual(user.last_name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attributes."""
        u = User()
        u.first_name = "Betty"
        u.last_name = "Bar"
        u.email = "airbnb@mail.com"
        u.password = "root"
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(new_d["first_name"], "Betty")
        self.assertEqual(new_d["last_name"], "Bar")
        self.assertEqual(new_d["email"], "airbnb@mail.com")
        self.assertEqual(new_d["password"], "root")

    def test_str(self):
        """Test that the str method has the correct output."""
        user = User()
        string = str(user)
        self.assertIn("[User]", string)
        self.assertIn(user.id, string)


if __name__ == '__main__':
    unittest.main()
