import tempfile
import unittest

from src.word_filter.remove import add_remove, add_remove_by

# See https://docs.python.org/3/library/unittest.html


animals = [
    "ant",
    "asp",
    "bass",
    "bat",
    "bee",
    "bird",
    "carp",
    "cat",
    "cod",
    "cow",
    "crab",
    "crow",
    "deer",
    "dog",
    "dove",
    "duck",
    "eel",
    "emu",
    "fly",
    "fox",
    "frog",
]

animal_str = "\n".join(animals)


class RemovalTests(unittest.TestCase):
    dir: tempfile.TemporaryDirectory[str]

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def check_rem(self, input: list[str], exclude: str, expected: list[str]):
        with self.subTest(msg="remove()", i=0):
            self.assertEqual(add_remove(exclude, None, input), expected)
        with self.subTest(msg="remove_by()", i=1):
            input2 = list(map(lambda a: [a], input))
            expected2 = list(map(lambda a: [a], expected))
            self.assertEqual(add_remove_by(exclude, None, input2, 0), expected2)

    def check_only(self, input: list[str], include: str, expected: list[str]):
        with self.subTest(msg="only()", i=0):
            self.assertEqual(add_remove(None, include, input), expected)

    def testRemoveHead(self):
        input = animals
        exclude = "\n".join(["ant", "asp"])
        expected = animals[2:]
        self.check_rem(input, exclude, expected)

    def testRemoveEnd(self):
        input = animals
        exclude = "\n".join(animals[-2:])
        expected = animals[:-2]
        self.check_rem(input, exclude, expected)

    def testRemoveMiddle(self):
        input = [
            "ant",
            "asp",
            "bass",
            "bat",
            "bee",
            "bird",
            "carp",
            "cat",
        ]
        exclude = "\n".join(["bat", "bee"])
        expected = [
            "ant",
            "asp",
            "bass",
            "bird",
            "carp",
            "cat",
        ]
        self.check_rem(input, exclude, expected)

    def testOnlyAddHead(self):
        input = animals[2:]
        include = animal_str
        expected = animals[2:]
        self.check_only(input, include, expected)

    def testOnlyAddHead2(self):
        input = animals
        include = "\n".join(animals[2:])
        expected = animals[2:]
        self.check_only(input, include, expected)

    def testOnlyAddEnd(self):
        input = animals[:-2]
        include = animal_str
        expected = animals[:-2]
        self.check_only(input, include, expected)

    def testOnlyAddEnd2(self):
        input = animals
        include = "\n".join(animals[:-2])
        expected = animals[:-2]
        self.check_only(input, include, expected)
