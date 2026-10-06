#!/usr/bin/python3
"""Unittest module for State class."""
import inspect
import unittest
import pycodestyle
import models
from models.base_model import BaseModel
from models.state import State


class TestStateDocs(unittest.TestCase):
    """Tests to check documentation and style of State class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.state_funcs = inspect.getmembers(
            State, inspect.isfunction
        )

    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_state(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_state.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_state_module_docstring(self):
        """Test for the state.py module docstring."""
        self.assertIsNotNone(
            models.state.__doc__,
            "state.py needs a docstring"
        )
        self.assertTrue(
            len(models.state.__doc__) >= 1,
            "state.py needs a docstring"
        )

    def test_state_class_docstring(self):
        """Test for the State class docstring."""
        self.assertIsNotNone(
            State.__doc__,
            "State class needs a docstring"
        )
        self.assertTrue(
            len(State.__doc__) >= 1,
            "State class needs a docstring"
        )


class TestState(unittest.TestCase):
    """Test cases for the State class."""

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel."""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute name, and it's an empty string."""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        self.assertEqual(state.name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attributes."""
        s = State()
        s.name = "California"
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(new_d["name"], "California")
        self.assertIsInstance(new_d["created_at"], str)
        self.assertIsInstance(new_d["updated_at"], str)

    def test_str(self):
        """Test that the str method has the correct output."""
        state = State()
        string = str(state)
        self.assertIn("[State]", string)
        self.assertIn(state.id, string)


if __name__ == '__main__':
    unittest.main()
