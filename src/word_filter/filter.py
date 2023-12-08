import argparse
import sys
import io
import random
from typing import Optional


def filter_words(
    infile: io.TextIOWrapper,
    min: int,
    max: int,
    chars: Optional[set[str]],
    lower: bool,
    sort: bool,
    shuffle: bool,
    limit: int,
    csv: bool,
    sep: Optional[str],
    csvfield: int,
    keepfields: bool,
) -> list[str]:
    words = []

    for line in infile:
        word = line.strip().lower() if lower else line.strip()
        if word == "":
            continue
        if csv:
            fields = word.split(sep)
            word = [x.strip() for x in fields if x.strip() != ""][csvfield].strip()
        if len(word) in range(min, max + 1) and (
            chars is None or all(c in chars for c in word)
        ):
            if csv and keepfields:
                words.append(line.strip())
            else:
                words.append(word)
            if limit > 0 and len(words) >= limit:
                break
    if sort:
        words.sort()
    elif shuffle:
        random.shuffle(words)
    return words


def write_words(words: list[str], outfile: io.TextIOWrapper):
    outfile.write("\n".join(words))


def main():
    parser = argparse.ArgumentParser(description="Filter words")
    parser.add_argument(
        "wordlist",
        metavar="infile",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Wordlist file; omit to use stdin",
        nargs="?",
    )
    parser.add_argument(
        "outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file; omit to write to stdout",
    )
    parser.add_argument(
        "-m",
        "--min",
        type=int,
        default=1,
        metavar="LENGTH",
        help="Include only words with at least LENGTH chars",
    )
    parser.add_argument(
        "-M",
        "--max",
        type=int,
        default=50,
        metavar="LENGTH",
        help="Include only words with at most LENGTH chars",
    )
    parser.add_argument(
        "-c", "--chars", default=None, help="Only include words with these letters"
    )
    parser.add_argument(
        "--no-lower",
        dest="lower",
        action="store_false",
        help="Do not convert words to lowercase",
    )
    parser.add_argument("--sort", action="store_true", help="Sort words alphabetically")
    parser.add_argument(
        "--shuffle", action="store_true", help="Randomly shuffle the wordlist"
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=0,
        metavar="MAXWORDS",
        help="Limit how many words are returned",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Treat the wordlist as a csv file",
    )
    parser.add_argument(
        "--sep",
        default=None,
        metavar="SEP",
        help="File is a csv deliminated by the specified character.  \\t specifies a tab character.  Default is any blank space.  Implies --csv",
    )
    parser.add_argument(
        "-f",
        "--field",
        default=None,
        type=int,
        metavar="COL",
        help="In a csv file, use the specified column number.  Starts at 0.  Default is 0.  Implies --csv",
    )
    parser.add_argument(
        "--header",
        action="store_true",
        help="skip the first line of the csv file",
    )
    parser.add_argument(
        "-k",
        "--keepfields",
        action="store_true",
        help="output all csv fields for matching lines instead of just the selected field",
    )
    args = parser.parse_args()

    if args.field is not None or args.sep is not None:
        args.csv = True

    if args.field is not None:
        args.field = args.field.replace("\\t", "\t")

    if args.csv == True and args.field is None:
        args.field = 0

    if args.csv and args.sep is None:
        line = args.wordlist.readline()
        if line.find(",") != -1:
            args.sep = ","
        elif line.find("\t") != -1:
            args.sep = "\t"
        args.wordlist.seek(0)

    if args.csv and args.header:
        header = args.wordlist.readline()
        if args.keepfields:
            args.outfile.write(header)

    chars = set(args.chars) if args.chars is not None else None
    words = filter_words(
        args.wordlist,
        args.min,
        args.max,
        chars,
        args.lower,
        args.sort,
        args.shuffle,
        args.limit,
        args.csv,
        args.sep,
        args.field,
        args.keepfields,
    )
    write_words(words, args.outfile)


if __name__ == "__main__":
    main()
