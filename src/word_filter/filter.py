import argparse
import sys
import io
import random
from typing import Optional


from .util import convert_nums
from .remove import remove, remove_by


def matches(
    word: str,
    min: int,
    max: int,
    chars: Optional[set[str]],
    required: Optional[set[str]],
) -> bool:
    return (
        len(word) in range(min, max + 1)
        and (chars is None or all(c in chars for c in word))
        and (required is None or any(c in required for c in word))
    )


def filter_words_list(
    infile: io.TextIOWrapper,
    min: int,
    max: int,
    chars: Optional[set[str]],
    required: Optional[set[str]],
    lower: bool,
    sort: bool,
    shuffle: bool,
    limit: int,
    exclude: Optional[io.TextIOWrapper],
) -> list[str]:
    words: list[str] = []
    for line in infile:
        word = line.strip().lower() if lower else line.strip()
        if word == "":
            continue
        if matches(word, min, max, chars, required):
            words.append(word)

    if exclude is not None:
        words = remove(exclude, words)
    elif sort:
        words.sort()

    if not sort and shuffle:
        random.shuffle(words)

    if limit > 0:
        return words[0:limit]
    return words


def filter_words_csv(
    infile: io.TextIOWrapper,
    min: int,
    max: int,
    chars: Optional[set[str]],
    required: Optional[set[str]],
    lower: bool,
    sort: bool,
    sortby: int,
    shuffle: bool,
    limit: int,
    sep: Optional[str],
    wordfield: int,
    keepfields: bool,
    exclude: Optional[io.TextIOWrapper],
) -> list[str]:
    words: list[list] = []
    for line in infile:
        line = line.strip().lower() if lower else line.strip()
        if line == "":
            continue
        fields = [f.strip() for f in line.split(sep)]
        if any(map(lambda s: s == "", fields)):
            fields = [f for f in fields if f != ""]

        word = fields[wordfield]
        if matches(word, min, max, chars, required):
            if sortby != wordfield:
                words.append(convert_nums(fields))
            else:
                words.append(fields)

    if exclude is not None:
        words = remove_by(exclude, words, wordfield)
    if sort and (not exclude or wordfield != sortby):
        words.sort(key=lambda a: a[sortby])
    if not sort and shuffle:
        random.shuffle(words)
    sep = sep if isinstance(sep, str) else ","
    if limit > 0:
        words = words[0:limit]
    if not keepfields:
        return [x[wordfield] for x in words]
    return [sep.join(w) for w in words]


def write_words(words: list[str], outfile: io.TextIOWrapper):
    outfile.write("\n".join(words))


def main():
    # print(sys.argv)

    parser = argparse.ArgumentParser(description="Filter words")
    parser.add_argument(
        "infile",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Wordlist file; omit to use stdin.",
        nargs="?",
    )
    parser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file; omit to write to stdout.",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=argparse.FileType("r"),
        default=None,
        metavar="FILE",
        help="Exclude any words found in this file.  This implies --sort.",
    )
    parser.add_argument(
        "-c",
        "--chars",
        default=None,
        metavar="CHARS",
        help="Words may only consist of the specified characters",
    )
    parser.add_argument(
        "-r",
        "--require",
        default=None,
        metavar="CHARS",
        help="All words must include at least one of these characters",
    )
    parser.add_argument(
        "-m",
        "--min",
        type=int,
        default=4,
        metavar="N",
        help="Include only words with at least LENGTH chars.  Default is 4.",
    )
    parser.add_argument(
        "-M",
        "--max",
        type=int,
        default=15,
        metavar="N",
        help="Include only words with at most LENGTH chars.  Default is 15.",
    )
    parser.add_argument(
        "--no-lower",
        dest="lower",
        action="store_false",
        help="Do not convert words to lowercase.",
    )
    parser.add_argument(
        "-s", "--sort", action="store_true", help="Sort words alphabetically."
    )
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help="Randomly shuffle the wordlist.  Ignored if --sort is also specified.",
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=0,
        metavar="N",
        help="Limit how many words are returned.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Treat the wordlist as a csv file.",
    )
    parser.add_argument(
        "--sortby",
        default=None,
        type=int,
        metavar="COL",
        help="Sort by the specified column number.  Starts at 0.",
    )
    parser.add_argument(
        "--sep",
        default=None,
        metavar="SEP",
        help="File is a csv deliminated by the specified character.  \\t specifies a tab character.  Default is any blank space.  Implies --csv.",
    )
    parser.add_argument(
        "-f",
        "--field",
        default=0,
        type=int,
        metavar="COL",
        help="In a csv file, use the specified column number as the word field.  Starts at 0.  Default is 0.  Implies --csv.",
    )
    parser.add_argument(
        "--header",
        action="store_true",
        help="Skip the first line of the csv file.  The header is removed from the output unless -k is also specified.",
    )
    parser.add_argument(
        "-k",
        "--keepfields",
        action="store_true",
        help="Output all csv fields for matching lines instead of just the selected field.",
    )
    args = parser.parse_args()

    if not args.csv:
        if args.field != 0 or args.sep is not None or args.header or args.keepfields:
            args.csv = True
        elif len(sys.argv) >= 2 and sys.argv[1].endswith(".csv"):
            args.csv = True

    if args.csv:
        if args.sep is None:
            line = args.infile.readline()
            if line.find(",") != -1:
                args.sep = ","
            elif line.find("\t") != -1:
                args.sep = "\t"
            args.infile.seek(0)
        if args.sep is not None:
            args.sep = args.sep.replace("\\t", "\t")

        if args.header:
            header = args.infile.readline()
            if args.keepfields:
                args.outfile.write(header)

        if args.sortby is None:
            args.sortby = args.field
        else:
            args.sort = True

    args.chars = set(args.chars) if args.chars is not None else None
    args.require = set(args.require) if args.require is not None else None

    if args.csv:
        words = filter_words_csv(
            args.infile,
            args.min,
            args.max,
            args.chars,
            args.require,
            args.lower,
            args.sort,
            args.sortby,
            args.shuffle,
            args.limit,
            args.sep,
            args.field,
            args.keepfields,
            args.exclude,
        )
    else:
        words = filter_words_list(
            args.infile,
            args.min,
            args.max,
            args.chars,
            args.require,
            args.lower,
            args.sort,
            args.shuffle,
            args.limit,
            args.exclude,
        )

    write_words(words, args.outfile)
    args.infile.close()
    args.outfile.close()
    if args.exclude is not None:
        args.exclude.close()


if __name__ == "__main__":
    main()
