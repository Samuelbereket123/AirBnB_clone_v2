#!/usr/bin/python3
"""Unittest module for Review class."""
import inspect
import unittest
import pycodestyle
import models
from models.base_model import BaseModel
from models.review import Review


class TestReviewDocs(unittest.TestCase):
    """Tests to check documentation and style of Review class."""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests."""
        cls.review_funcs = inspect.getmembers(
            Review, inspect.isfunction
        )

    def test_pep8_conformance_review(self):
        """Test that models/review.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_review(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_review.py']
        )
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings)."
        )

    def test_review_module_docstring(self):
        """Test for the review.py module docstring."""
        self.assertIsNotNone(
            models.review.__doc__,
            "review.py needs a docstring"
        )
        self.assertTrue(
            len(models.review.__doc__) >= 1,
            "review.py needs a docstring"
        )

    def test_review_class_docstring(self):
        """Test for the Review class docstring."""
        self.assertIsNotNone(
            Review.__doc__,
            "Review class needs a docstring"
        )
        self.assertTrue(
            len(Review.__doc__) >= 1,
            "Review class needs a docstring"
        )


class TestReview(unittest.TestCase):
    """Test cases for the Review class."""

    def test_is_subclass(self):
        """Test that Review is a subclass of BaseModel."""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Test Review has attr place_id, and it's an empty string."""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        self.assertEqual(review.place_id, "")

    def test_user_id_attr(self):
        """Test Review has attr user_id, and it's an empty string."""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        self.assertEqual(review.user_id, "")

    def test_text_attr(self):
        """Test Review has attr text, and it's an empty string."""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        self.assertEqual(review.text, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attributes."""
        r = Review()
        r.place_id = "place-123"
        r.user_id = "user-456"
        r.text = "Great place to stay!"
        new_d = r.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(new_d["place_id"], "place-123")
        self.assertEqual(new_d["user_id"], "user-456")
        self.assertEqual(new_d["text"], "Great place to stay!")
        self.assertIsInstance(new_d["created_at"], str)
        self.assertIsInstance(new_d["updated_at"], str)

    def test_str(self):
        """Test that the str method has the correct output."""
        review = Review()
        string = str(review)
        self.assertIn("[Review]", string)
        self.assertIn(review.id, string)


if __name__ == '__main__':
    unittest.main()
