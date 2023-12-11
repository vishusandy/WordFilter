import tempfile
import unittest

from src.word_filter.remove import remove_by, remove

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


class RemovalTests(unittest.TestCase):
    dir: tempfile.TemporaryDirectory[str]

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def check(self, input: list[str], exclude: str, expected: list[str]):
        with self.subTest(msg="remove()", i=0):
            self.assertEqual(remove(exclude, input), expected)
        with self.subTest(msg="remove_by()", i=1):
            input2 = list(map(lambda a: [a], input))
            expected2 = list(map(lambda a: [a], expected))
            self.assertEqual(remove_by(exclude, input2, 0), expected2)

    def testRemoveHead(self):
        input = animals
        exclude = "\n".join(["ant", "asp"])
        expected = animals[2:]
        self.check(input, exclude, expected)

    def testRemoveEnd(self):
        input = animals
        exclude = "\n".join(animals[-2:])
        expected = animals[:-2]
        self.check(input, exclude, expected)

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
        self.check(input, exclude, expected)
