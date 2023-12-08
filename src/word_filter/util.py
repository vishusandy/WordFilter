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


def num(s: str) -> str | int | float:
    if is_int(s):
        return int(s)
    if is_float(s):
        return float(s)
    return s


def convert_nums(fields: list[str]) -> list[str | float | int]:
    return [num(f) for f in fields]
