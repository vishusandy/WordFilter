from pathlib import Path
import re
import struct

is_64bit = struct.calcsize("P") * 8 == 64

re_is_float = re.compile("^-?[0-9.]+$")
re_is_int = re.compile("^-?[0-9]{1,19}$") if is_64bit else re.compile("^-?[0-9]{1,10}$")


def is_int(s: str):
    return re_is_int.match(s) is not None


def is_float(s: str):
    return re_is_float.match(s) is not None and s.count(".") <= 1


def add_prefix(prefix: str, file: str) -> str:
    p = Path(file)
    s = str(p)[len(p.anchor) :]
    return str(Path(prefix) / s)
