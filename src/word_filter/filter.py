import random
from typing import Optional

from .util import convert_nums, tier_fields, CommonArgs
from .remove import remove, remove_by
from . import errors


def filter_words_list(args: CommonArgs) -> list[str]:
    words: list[str] = []
    for line in args.infile:
        word = line.strip().lower() if args.lower else line.strip()
        if word == "":
            continue

        if args.matches(word):
            words.append(word)

    if args.exclude is not None:
        words = remove(args.exclude, words)
    elif args.sort:
        words.sort()

    if not args.sort and args.shuffle:
        random.shuffle(words)

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
    wfa = 0  # word field adjustment
    use_weights = weight is not None and len(weight) != 0
    if use_weights:
        # sortby += 2
        wfa = 2

    for line in args.infile:
        line = line.strip().lower() if args.lower else line.strip()
        if line == "":
            continue
        if weight is None or len(weight) == 0:
            fields: list = [f.strip() for f in line.split(sep)]
        else:
            tmp = [f.strip() for f in line.split(sep)]
            fields = tier_fields(tmp[wordfield], weight) + tmp
        if len(fields) == 0:
            continue
        if any(map(lambda s: s == "", fields)):
            fields = [f for f in fields if f != ""]

        if not isinstance(fields[wordfield + wfa], str):
            raise errors.InternalError("attempting to use non-str field for word field")
        if args.matches(fields[wordfield + wfa]):
            if sortby != wordfield + wfa:
                words.append(convert_nums(fields))
            else:
                words.append(fields)

    if args.exclude is not None:
        words = remove_by(args.exclude, words, wordfield + wfa)
    if args.sort and (not args.exclude or wordfield + wfa != sortby):
        words.sort(key=lambda a: a[sortby])
    if not args.sort and args.shuffle:
        random.shuffle(words)
    sep = sep if isinstance(sep, str) else ","
    if args.limit > 0:
        words = words[0 : args.limit]
    if not keepfields:
        return [x[wordfield + wfa] for x in words]
    return [realsep.join([str(f) for f in w]) for w in words]
