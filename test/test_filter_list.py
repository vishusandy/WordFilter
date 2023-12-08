import unittest
import tempfile

from .filter_base import FilterBase

# See https://docs.python.org/3/library/unittest.html


class FilterTests(FilterBase):
    dir: tempfile.TemporaryDirectory[str]

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def testSameInOut(self):
        input = "\n".join(["bear", "bird", "cheetah", "duck"])
        input_file = self.add("input.txt", input)

        output_file = "output.txt"
        self.patch(input_file, output_file)()

        self.assertEqual(self.has(output_file), input)

    def testExclude(self):
        input = "\n".join(["bear", "bird", "cheetah", "duck"])
        input_file = self.add("input.txt", input)

        exclude = "cheetah"
        exclude_file = self.add("exclude.txt", exclude)

        expected_output = "\n".join(["bear", "bird", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "-x", str(exclude_file))()

        self.assertEqual(self.has(output_file), expected_output)

    def testChars(self):
        input = "\n".join(["bear", "birds", "cheetah", "duck"])
        input_file = self.add("input.txt", input)

        chars = "abcehrt"
        expected_output = "\n".join(["bear", "cheetah"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "-c", chars)()

        self.assertEqual(self.has(output_file), expected_output)

    def testRequiredChars(self):
        input = "\n".join(["bear", "birds", "cheetah", "duck"])
        input_file = self.add("input.txt", input)

        chars = "b"
        expected_output = "\n".join(["bear", "birds"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--require", chars)()

        self.assertEqual(self.has(output_file), expected_output)

    def testNoLower(self):
        input = "\n".join(["Bear", "bIrds", "chEEtaH", "DucK"])
        input_file = self.add("input.txt", input)

        output_file = "output.txt"
        self.patch(input_file, output_file, "--no-lower")()

        self.assertEqual(self.has(output_file), input)

    def testSort(self):
        input = "\n".join(["cheetah", "birds", "duck", "bear"])
        input_file = self.add("input.txt", input)

        expected_output = "\n".join(["bear", "birds", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--sort")()

        self.assertEqual(self.has(output_file), expected_output)

    def testMin(self):
        input = "\n".join(["bear", "birds", "cheetah", "duck"])
        input_file = self.add("input.txt", input)

        expected_output = "\n".join(["birds", "cheetah"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "-m 5")()

        self.assertEqual(self.has(output_file), expected_output)

    def testMax(self):
        input = "\n".join(["bear", "bird", "cheetah", "duck"])
        input_file = self.add("input.txt", input)

        expected_output = "\n".join(["bear", "bird", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "-M 4")()

        self.assertEqual(self.has(output_file), expected_output)

    def testLimit(self):
        input = "\n".join(["bear", "bird", "cheetah", "duck"])
        input_file = self.add("input.txt", input)

        expected_output = "\n".join(["bear", "bird", "cheetah"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "-n 3")()

        self.assertEqual(self.has(output_file), expected_output)


if __name__ == "__main__":
    unittest.main()
