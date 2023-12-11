from dataclasses import dataclass
import io
from pathlib import Path
import re
import struct
from typing import Optional

_is_64bit = struct.calcsize("P") * 8 == 64
_re_float = re.compile("^-?[0-9.]+$")
_re_int = re.compile("^-?[0-9]{1,19}$") if _is_64bit else re.compile("^-?[0-9]{1,10}$")


def is_int(s: str):
    return _re_int.match(s) is not None


def is_float(s: str):
    return _re_float.match(s) is not None and s.count(".") <= 1


def add_prefix(prefix: str, file: str) -> str:
    p = Path(file)
    s = str(p)[len(p.anchor) :]
    return str(Path(prefix) / s)


def _num(s: str | int | float) -> str | int | float:
    if isinstance(s, int) or isinstance(s, float):
        return s
    if is_int(s):
        return int(s)
    if is_float(s):
        return float(s)
    return s


def convert_nums(fields: list) -> list[str | float | int]:
    return [_num(f) for f in fields]


@dataclass
class CommonArgs:
    infile: io.TextIOWrapper
    exclude: Optional[io.TextIOWrapper]
    include: Optional[io.TextIOWrapper]
    min: int
    max: int
    chars: Optional[set[str]]
    required: Optional[set[str]]
    lower: bool
    sort: bool
    shuffle: bool
    limit: int

    def matches(self, word: str) -> bool:
        return (
            len(word) in range(self.min, self.max + 1)
            and (self.chars is None or all(c in self.chars for c in word))
            and (self.required is None or any(c in self.required for c in word))
        )


def tier_fields(word: str, weight: list[str]) -> list[float]:
    m = float(pow(2, len(weight)) - 1.0)  # max rank
    rank = 0.0  # tier rank
    w = 0.0  # weight (% contained in each tier)
    p = 0  # previous tier
    for i, chars in enumerate(weight):
        ws = [c in chars for c in word]
        if any(ws):
            t = pow(2, i)
            r = t / m  # tier percentage
            rank += r
            percent = ws.count(True) / len(word)
            w += (r - p) * percent + p
            p = t
    return [rank, w]
