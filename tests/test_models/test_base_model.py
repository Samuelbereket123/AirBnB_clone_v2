#!/usr/bin/python3
"""Unittest module for BaseModel class."""
import inspect
import os
import time
import unittest
from datetime import datetime
import pycodestyle
import models
from models.base_model import BaseModel


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check documentation and style of BaseModel class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.base_funcs = inspect.getmembers(
            BaseModel, inspect.isfunction
        )

    def test_pep8_conformance_base_model(self):
        """Test that models/base_model.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_base_model(self):
        """Test that tests/test_models/test_base_model.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_base_model.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_base_model_module_docstring(self):
        """Test for the base_model.py module docstring."""
        self.assertIsNotNone(
            models.base_model.__doc__,
            "base_model.py needs a docstring"
        )
        self.assertTrue(
            len(models.base_model.__doc__) >= 1,
            "base_model.py needs a docstring"
        )

    def test_base_model_class_docstring(self):
        """Test for the BaseModel class docstring."""
        self.assertIsNotNone(
            BaseModel.__doc__,
            "BaseModel class needs a docstring"
        )
        self.assertTrue(
            len(BaseModel.__doc__) >= 1,
            "BaseModel class needs a docstring"
        )

    def test_base_model_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods."""
        for func in self.base_funcs:
            self.assertIsNotNone(
                func[1].__doc__,
                "{:s} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0])
            )


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def test_instance_creation(self):
        """Test instantiation of BaseModel."""
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_unique_id(self):
        """Test that two instances have unique IDs."""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_init_with_kwargs(self):
        """Test instantiation with keyword arguments."""
        dt = datetime.now()
        dt_iso = dt.isoformat()
        model = BaseModel(
            id="1234-5678",
            created_at=dt_iso,
            updated_at=dt_iso,
            name="TestModel"
        )
        self.assertEqual(model.id, "1234-5678")
        self.assertEqual(model.created_at, dt)
        self.assertEqual(model.updated_at, dt)
        self.assertEqual(model.name, "TestModel")

    def test_init_with_args_and_kwargs(self):
        """Test instantiation with args and kwargs."""
        model = BaseModel(
            "unused_arg",
            id="test-id-123",
            name="MyModel"
        )
        self.assertEqual(model.id, "test-id-123")
        self.assertEqual(model.name, "MyModel")

    def test_to_dict(self):
        """Test dictionary representation method."""
        model = BaseModel()
        model.name = "My First Model"
        model.my_number = 89
        model_dict = model.to_dict()
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['name'], 'My First Model')
        self.assertEqual(model_dict['my_number'], 89)
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertEqual(
            model_dict['created_at'], model.created_at.isoformat()
        )
        self.assertEqual(
            model_dict['updated_at'], model.updated_at.isoformat()
        )

    def test_to_dict_type(self):
        """Test that to_dict returns a valid dictionary copy."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIsNot(model_dict, model.__dict__)

    def test_str(self):
        """Test string representation output."""
        model = BaseModel()
        string = str(model)
        self.assertIn("[BaseModel]", string)
        self.assertIn(model.id, string)
        self.assertIn(str(model.__dict__), string)

    def test_save(self):
        """Test save method updates updated_at datetime."""
        model = BaseModel()
        old_updated_at = model.updated_at
        time.sleep(0.01)
        model.save()
        self.assertGreater(model.updated_at, old_updated_at)


if __name__ == '__main__':
    unittest.main()
