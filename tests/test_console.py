#!/usr/bin/python3
"""Unittest module for the HBNB console."""
import inspect
import io
import os
import unittest
from unittest.mock import patch
import pycodestyle
import console
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestConsoleDocs(unittest.TestCase):
    """Tests to check documentation and style of console."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.console_funcs = [
            member for member in inspect.getmembers(
                HBNBCommand, inspect.isfunction
            ) if member[1].__module__ == 'console'
        ]

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_console.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_console_module_docstring(self):
        """Test for the console.py module docstring."""
        self.assertIsNotNone(
            console.__doc__,
            "console.py needs a docstring"
        )
        self.assertTrue(
            len(console.__doc__) >= 1,
            "console.py needs a docstring"
        )

    def test_hbnb_command_class_docstring(self):
        """Test for the HBNBCommand class docstring."""
        self.assertIsNotNone(
            HBNBCommand.__doc__,
            "HBNBCommand class needs a docstring"
        )
        self.assertTrue(
            len(HBNBCommand.__doc__) >= 1,
            "HBNBCommand class needs a docstring"
        )

    def test_console_func_docstrings(self):
        """Test for the presence of docstrings in HBNBCommand methods."""
        for func in self.console_funcs:
            self.assertIsNotNone(
                func[1].__doc__,
                "{:s} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0])
            )


class TestConsoleCommands(unittest.TestCase):
    """Test cases for HBNBCommand command interpreter."""

    def setUp(self):
        """Set up test environment."""
        self.cli = HBNBCommand()

    def test_prompt(self):
        """Test prompt string."""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        """Test emptyline method does nothing."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.emptyline()
            self.assertEqual("", fake_out.getvalue())

    def test_quit(self):
        """Test quit command exits."""
        self.assertTrue(self.cli.do_quit(""))

    def test_EOF(self):
        """Test EOF command exits."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.assertTrue(self.cli.do_EOF(""))
            self.assertEqual("\n", fake_out.getvalue())

    def test_create_missing_class(self):
        """Test create without class name."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create("")
            self.assertEqual(
                "** class name missing **\n", fake_out.getvalue()
            )

    def test_create_invalid_class(self):
        """Test create with non-existent class."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create("MyFakeModel")
            self.assertEqual(
                "** class doesn't exist **\n", fake_out.getvalue()
            )

    def test_create_valid_class(self):
        """Test create with valid class name."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create("BaseModel")
            obj_id = fake_out.getvalue().strip()
            key = "BaseModel." + obj_id
            self.assertIn(key, storage.all())

    def test_create_params_string(self):
        """Test create with string parameters."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create('State name="California"')
            obj_id = fake_out.getvalue().strip()
            key = "State." + obj_id
            self.assertIn(key, storage.all())
            self.assertEqual(storage.all()[key].name, "California")

    def test_create_params_string_spaces(self):
        """Test create with string parameter containing underscores."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create('State name="My_little_house"')
            obj_id = fake_out.getvalue().strip()
            key = "State." + obj_id
            self.assertIn(key, storage.all())
            self.assertEqual(storage.all()[key].name, "My little house")

    def test_create_params_string_escaped_quotes(self):
        """Test create with string containing escaped quotes."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create('State name="My_\\"sweet\\"_home"')
            obj_id = fake_out.getvalue().strip()
            key = "State." + obj_id
            self.assertIn(key, storage.all())
            self.assertEqual(storage.all()[key].name, 'My "sweet" home')

    def test_create_params_int(self):
        """Test create with integer parameters."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create('Place number_rooms=4 max_guest=10')
            obj_id = fake_out.getvalue().strip()
            key = "Place." + obj_id
            self.assertIn(key, storage.all())
            self.assertEqual(storage.all()[key].number_rooms, 4)
            self.assertEqual(storage.all()[key].max_guest, 10)

    def test_create_params_float(self):
        """Test create with float parameters."""
        cmd = 'Place latitude=37.773972 longitude=-122.431297'
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create(cmd)
            obj_id = fake_out.getvalue().strip()
            key = "Place." + obj_id
            self.assertIn(key, storage.all())
            self.assertEqual(storage.all()[key].latitude, 37.773972)
            self.assertEqual(storage.all()[key].longitude, -122.431297)

    def test_create_params_all_types(self):
        """Test create with all parameter types combined."""
        cmd = (
            'Place city_id="0001" user_id="0001" name="My_little_house" '
            'number_rooms=4 number_bathrooms=2 max_guest=10 '
            'price_by_night=300 latitude=37.773972 longitude=-122.431297'
        )
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create(cmd)
            obj_id = fake_out.getvalue().strip()
            key = "Place." + obj_id
            self.assertIn(key, storage.all())
            obj = storage.all()[key]
            self.assertEqual(obj.city_id, "0001")
            self.assertEqual(obj.user_id, "0001")
            self.assertEqual(obj.name, "My little house")
            self.assertEqual(obj.number_rooms, 4)
            self.assertEqual(obj.number_bathrooms, 2)
            self.assertEqual(obj.max_guest, 10)
            self.assertEqual(obj.price_by_night, 300)
            self.assertEqual(obj.latitude, 37.773972)
            self.assertEqual(obj.longitude, -122.431297)

    def test_create_params_invalid_skipped(self):
        """Test create skips malformed parameters."""
        cmd = (
            'State name="California" invalid_float=3.14.15 '
            'unclosed="test bad'
        )
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_create(cmd)
            obj_id = fake_out.getvalue().strip()
            key = "State." + obj_id
            self.assertIn(key, storage.all())
            obj = storage.all()[key]
            self.assertEqual(obj.name, "California")
            self.assertFalse(hasattr(obj, "invalid_float"))
            self.assertFalse(hasattr(obj, "unclosed"))
            self.assertFalse(hasattr(obj, "bad"))

    def test_show_missing_class(self):
        """Test show without class name."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_show("")
            self.assertEqual(
                "** class name missing **\n", fake_out.getvalue()
            )

    def test_show_invalid_class(self):
        """Test show with invalid class."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_show("FakeClass 123")
            self.assertEqual(
                "** class doesn't exist **\n", fake_out.getvalue()
            )

    def test_show_missing_id(self):
        """Test show with missing instance id."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_show("BaseModel")
            self.assertEqual(
                "** instance id missing **\n", fake_out.getvalue()
            )

    def test_show_invalid_id(self):
        """Test show with non-existent instance id."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_show("BaseModel 999999")
            self.assertEqual(
                "** no instance found **\n", fake_out.getvalue()
            )

    def test_show_valid(self):
        """Test show with valid class and id."""
        bm = BaseModel()
        bm.save()
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_show("BaseModel {}".format(bm.id))
            self.assertIn(bm.id, fake_out.getvalue())

    def test_destroy_missing_class(self):
        """Test destroy without class name."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_destroy("")
            self.assertEqual(
                "** class name missing **\n", fake_out.getvalue()
            )

    def test_destroy_invalid_class(self):
        """Test destroy with invalid class."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_destroy("FakeClass 123")
            self.assertEqual(
                "** class doesn't exist **\n", fake_out.getvalue()
            )

    def test_destroy_missing_id(self):
        """Test destroy with missing instance id."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_destroy("BaseModel")
            self.assertEqual(
                "** instance id missing **\n", fake_out.getvalue()
            )

    def test_destroy_invalid_id(self):
        """Test destroy with non-existent instance id."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_destroy("BaseModel 999999")
            self.assertEqual(
                "** no instance found **\n", fake_out.getvalue()
            )

    def test_destroy_valid(self):
        """Test destroy with valid class and id."""
        bm = BaseModel()
        bm.save()
        key = "BaseModel." + bm.id
        with patch('sys.stdout', new=io.StringIO()):
            self.cli.do_destroy("BaseModel {}".format(bm.id))
        self.assertNotIn(key, storage.all())

    def test_all_invalid_class(self):
        """Test all with non-existent class."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_all("FakeClass")
            self.assertEqual(
                "** class doesn't exist **\n", fake_out.getvalue()
            )

    def test_all_valid_class(self):
        """Test all with valid class."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_all("State")
            self.assertIn("[", fake_out.getvalue())

    def test_update_missing_class(self):
        """Test update with missing class name."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_update("")
            self.assertEqual(
                "** class name missing **\n", fake_out.getvalue()
            )

    def test_update_invalid_class(self):
        """Test update with invalid class."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_update("FakeClass 123")
            self.assertEqual(
                "** class doesn't exist **\n", fake_out.getvalue()
            )

    def test_update_missing_id(self):
        """Test update with missing id."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_update("BaseModel")
            self.assertEqual(
                "** instance id missing **\n", fake_out.getvalue()
            )

    def test_update_invalid_id(self):
        """Test update with invalid id."""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_update("BaseModel 999999")
            self.assertEqual(
                "** no instance found **\n", fake_out.getvalue()
            )

    def test_update_missing_attr_name(self):
        """Test update with missing attribute name."""
        bm = BaseModel()
        bm.save()
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_update("BaseModel {}".format(bm.id))
            self.assertEqual(
                "** attribute name missing **\n", fake_out.getvalue()
            )

    def test_update_missing_value(self):
        """Test update with missing value."""
        bm = BaseModel()
        bm.save()
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.cli.do_update("BaseModel {} name".format(bm.id))
            self.assertEqual(
                "** value missing **\n", fake_out.getvalue()
            )

    def test_update_valid(self):
        """Test update with valid parameters."""
        bm = BaseModel()
        bm.save()
        with patch('sys.stdout', new=io.StringIO()):
            self.cli.do_update(
                'BaseModel {} first_name "Betty"'.format(bm.id)
            )
        self.assertEqual(getattr(bm, "first_name", None), "Betty")


if __name__ == '__main__':
    unittest.main()
