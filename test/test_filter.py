import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import sys
from collections.abc import Callable

from src.word_filter.filter import main as word_filter
from src.word_filter.util import is_int, is_float, add_prefix

# See https://docs.python.org/3/library/unittest.html


# Command line arguments with unittest:
#   https://stackoverflow.com/questions/70757534/how-to-unittest-with-command-line-arguments


def set_sys_argv(*argv):
    sys.argv = argv

    def _decorator(func: Callable):
        def wrapper(*args, **kwargs):
            func()

        return wrapper

    return _decorator


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


class FilterTests(unittest.TestCase):
    dir: tempfile.TemporaryDirectory[str]

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def add(self, filename: str, contents: str) -> Path:
        path = Path(self.dir.name) / filename
        with open(path, "wt") as f:
            f.write(contents)
            f.close()
        return path

    def has(self, filename: str | Path) -> str:
        if isinstance(filename, Path):
            path = filename
        else:
            path = Path(self.dir.name) / filename
        with open(path, "rt") as f:
            s = f.read()
            f.close()
            return s

    def args(self, infile: str | Path | None, outfile: str | Path | None, *args):
        output: list[str] = ["test_filter.py"]

        if isinstance(infile, Path):
            output.append(str(infile))
        elif isinstance(infile, str):
            p = Path(add_prefix(self.dir.name, infile))
            output.append(str(p))

        if isinstance(outfile, Path):
            print("outfile is Path")
            output.append(str(outfile))
        elif isinstance(outfile, str):
            p = Path(add_prefix(self.dir.name, outfile))
            output.append(str(p))

        for arg in args:
            if isinstance(arg, tuple):
                output.extend(arg)
            else:
                output.append(arg)
        return output

    def patch(self, infile: str | Path | None, outfile: str | Path | None, *args):
        args = self.args(infile, outfile, args)

        @patch("sys.argv", args)
        def _wrapper():
            word_filter()

        return _wrapper

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

    def testCsv(self):
        input = "\n".join(["bear,1.5", "bird,1.6", "cheetah,1.7", "duck,1.8"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvAuto(self):
        input = "\n".join(["bear,1.5", "bird,1.6", "cheetah,1.7", "duck,1.8"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file)()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvExclude(self):
        input = "\n".join(["bear,4", "bird,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        exclude = "cheetah"
        exclude_file = self.add("exclude.txt", exclude)

        expected_output = "\n".join(["bear", "bird", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-x", str(exclude_file))()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvChars(self):
        input = "\n".join(["bear,4", "birds,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        chars = "abcehrt"
        expected_output = "\n".join(["bear", "cheetah"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-c", chars)()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvNoLower(self):
        input = "\n".join(["Bear,4", "bIrds,4", "chEEtaH,4", "DucK,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["Bear", "bIrds", "chEEtaH", "DucK"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--no-lower")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSort(self):
        input = "\n".join(["cheetah,4", "birds,4", "duck,4", "bear,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "birds", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--sort")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSort2(self):
        input = "\n".join(["4,cheetah", "3,birds", "2,duck", "1,bear"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "birds", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-f 1", "--sort")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvMin(self):
        input = "\n".join(["bear,4", "birds,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["birds", "cheetah"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-m 5")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvMax(self):
        input = "\n".join(["bear,4", "bird,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-M 4")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvLimit(self):
        input = "\n".join(["bear,4", "bird,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-n 3")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvHeader(self):
        input = "\n".join(["animal,number", "bear,4", "bird,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--header")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvHeaderKeepFields(self):
        input = "\n".join(["animal,number", "bear,4", "bird,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(
            ["animal,number", "bear,4", "bird,4", "cheetah,4", "duck,4"]
        )

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--header", "-k")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvKeepFields(self):
        input = "\n".join(["bear,4", "bird,4", "cheetah,4", "duck,4"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear,4", "bird,4", "cheetah,4", "duck,4"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-k")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSortBy(self):
        input = "\n".join(["bear,4", "bird,2", "cheetah,1", "duck,3"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["cheetah", "bird", "duck", "bear"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--sortby", "1")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSortByInt(self):
        input = "\n".join(["bear,4", "bird,2", "cheetah,10", "duck,3"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bird", "duck", "bear", "cheetah"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--sortby", "1")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSortByFloat(self):
        input = "\n".join(["bear,40.0", "bird,0400.0", "cheetah,10.0", "duck,30.0"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["cheetah", "duck", "bear", "bird"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--sortby", "1")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvField(self):
        input = "\n".join(["4,bear", "2,bird", "1,cheetah", "3,duck"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "-f", "1")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSeparatorTab(self):
        input = "\n".join(["bear\t\t4", "bird\t2", "cheetah\t1", "duck\t3"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--sep", "\\t")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSeparatorTabAuto(self):
        input = "\n".join(["bear\t4", "bird\t2", "cheetah\t\t1", "duck\t3"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv")()

        self.assertEqual(self.has(output_file), expected_output)

    def testCsvSeparatorSpaces(self):
        input = "\n".join(["bear   4", "bird   2", "cheetah  1", "duck 3"])
        input_file = self.add("input.csv", input)

        expected_output = "\n".join(["bear", "bird", "cheetah", "duck"])

        output_file = "output.txt"
        self.patch(input_file, output_file, "--csv", "--sep", " ")()

        self.assertEqual(self.has(output_file), expected_output)


if __name__ == "__main__":
    unittest.main()
