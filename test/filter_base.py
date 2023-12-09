import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile

from src.word_filter.main import main as word_filter
from src.word_filter.util import add_prefix

# See https://docs.python.org/3/library/unittest.html


# Command line arguments with unittest:
#   https://stackoverflow.com/questions/70757534/how-to-unittest-with-command-line-arguments


class FilterBase(unittest.TestCase):
    dir: tempfile.TemporaryDirectory[str]

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
