import unittest

from src.word_filter.util import is_int, is_float

# from src.word_filter.main import foo

# See https://docs.python.org/3/library/unittest.html


class NumberTests(unittest.TestCase):
    def testIsInt(self):
        self.assertTrue(is_int("-5000"))
        self.assertTrue(is_int("500"))

        self.assertFalse(is_int("50a0"))

    def testIsFloat(self):
        self.assertTrue(is_float("4000"))
        self.assertTrue(is_float("-400"))
        self.assertTrue(is_float("40.00"))

        self.assertFalse(is_float("40.0.0"))
        self.assertFalse(is_float("40a0"))


if __name__ == "__main__":
    unittest.main()
