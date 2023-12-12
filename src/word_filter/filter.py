import random
from typing import Optional

from .util import convert_nums, tier_fields, CommonArgs
from .remove import add_remove, add_remove_by
from . import errors


def filter_words_list(args: CommonArgs) -> list[str]:
    words: list[str] = []
    for line in args.infile:
        word = line.strip().lower() if args.lower else line.strip()
        if word == "":
            continue

        if args.matches(word):
            words.append(word)

    words = add_remove(args.exclude, args.include, words)

    if args.sort:
        words.sort()
    elif args.shuffle:
        random.shuffle(words)

    if args.reverse:
        words.reverse()
    if args.limit > 0:
        return words[0 : args.limit]
    return words


def filter_words_csv(
    args: CommonArgs,
    sortby: int,
    sep: Optional[str],
    wordfield: int,
    keepfields: bool,
    weight: Optional[list[str]],
) -> list[str]:
    words: list[list] = []
    realsep = sep if sep is not None else "\t"
    adj = 0 if weight is None else 2  # word field adjustment

    for line in args.infile:
        line = line.strip().lower() if args.lower else line.strip()
        if line == "":
            continue

        if weight is None:
            fields: list = [f.strip() for f in line.split(sep)]
        else:
            tmp = [f.strip() for f in line.split(sep)]
            fields = tier_fields(tmp[wordfield], weight) + tmp

        if len(fields) == 0:
            continue
        if any(map(lambda s: s == "", fields)):
            fields = [f for f in fields if f != ""]

        if not isinstance(fields[wordfield + adj], str):
            raise errors.InternalError("attempting to use non-str field for word field")
        if args.matches(fields[wordfield + adj]):
            if sortby != wordfield + adj:
                words.append(convert_nums(fields))
            else:
                words.append(fields)

    words = add_remove_by(args.exclude, args.include, words, wordfield + adj)

    if args.sort:
        words.sort(key=lambda a: a[sortby])
    elif args.shuffle:
        random.shuffle(words)

    if args.reverse:
        words.reverse()
    sep = sep if isinstance(sep, str) else ","
    if args.limit > 0:
        words = words[0 : args.limit]
    if not keepfields:
        return [x[wordfield + adj] for x in words]
    return [realsep.join([str(f) for f in w]) for w in words]
