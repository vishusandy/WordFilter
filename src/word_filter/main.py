import argparse
import io
import sys

from .util import CommonArgs
from .filter import filter_words_csv, filter_words_list
from . import errors


def write_words(words: list[str], outfile: io.TextIOWrapper):
    outfile.write("\n".join(words))


def process_args(args: argparse.Namespace):
    if args.csv == False:
        if (
            args.field != 0
            or args.sep is not None
            or args.header
            or args.keepfields
            or args.sortby is not None
            or args.weight is not None
        ):
            args.csv = True
        elif args.infile is not None and args.infile.name.endswith(".csv"):
            args.csv = True

    if args.csv:
        if args.sep is None:
            line = args.infile.readline()
            if line.find(",") != -1:
                args.sep = ","
            args.infile.seek(0)
        if args.sep is not None:
            args.sep = args.sep.replace("\\t", "\t")

        if args.header:
            header = args.infile.readline()
            if args.keepfields:
                if args.weight is not None:
                    tmpsep = args.sep if args.sep is not None else "\t"
                    args.outfile.write(
                        "tier_rank" + tmpsep + "tier_weight" + tmpsep + header
                    )
                else:
                    args.outfile.write(header)

        if args.weight is not None:
            # print(f"weights={args.weight} flattened={sum(args.weight, [])}")
            args.weight = [w for w in sum(args.weight, []) if w != ""]
            l = len(args.weight)
            if l == 0:
                args.weight = None
            elif l >= 31:
                raise errors.TooManyWeights(l, 30)

        if args.sortby is None:
            if args.weight is not None:
                args.sortby = 1
            else:
                args.sortby = args.field
        else:
            if args.sortby < 0:
                raise errors.UnexpectedNegativeValue("sortby", args.sortby)
            args.sort = True

    args.chars = set(args.chars) if args.chars is not None else None
    args.required = set(args.required) if args.required is not None else None

    return args


def main():
    # print(sys.argv)

    parser = argparse.ArgumentParser(description="Filter and sort a list of words.")
    csv_args = parser.add_argument_group("csv")
    parser.add_argument(
        "infile",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Wordlist file; omit to use stdin.  Each word must be on its own line.",
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
        "-c",
        "--chars",
        default=None,
        metavar="CHARS",
        help="Words may only consist of the specified characters",
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
        "-n",
        "--limit",
        type=int,
        default=0,
        metavar="N",
        help="Limit how many words are returned.",
    )
    parser.add_argument(
        "-r",
        "--require",
        dest="required",
        default=None,
        metavar="CHARS",
        help="All words must include at least one of these characters",
    )
    parser.add_argument(
        "-s", "--sort", action="store_true", help="Sort words alphabetically."
    )
    parser.add_argument(
        "-w",
        "--weight",
        default=None,
        nargs="*",
        metavar="CHARS",
        action="append",
        help="Adds another weight tier with the given characters.  This can be specified multiple times.  The first -w will be the lowest tier, with the last -w being the highest ranking tier.",
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
        "--no-lower",
        dest="lower",
        action="store_false",
        help="Do not convert words to lowercase.",
    )
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help="Randomly shuffle the wordlist.  Ignored if --sort is also specified.",
    )

    csv_args.add_argument(
        "--csv",
        action="store_true",
        help="Treat the wordlist as a csv file.  Can be used with a regular word list that does not have multiple fields.",
    )
    csv_args.add_argument(
        "-f",
        "--field",
        default=0,
        type=int,
        metavar="COL",
        help="In a csv file, use the specified column number as the word field.  Starts at 0.  Defaults to 0.  Implies --csv.",
    )
    csv_args.add_argument(
        "-k",
        "--keepfields",
        action="store_true",
        help="Output all csv fields for matching lines instead of just the selected field.  Implies --csv.",
    )
    csv_args.add_argument(
        "--sortby",
        default=None,
        type=int,
        metavar="COL",
        help="Sort by the specified column number.  Starts at 0.  Defaults to 0.  This value must be adjusted (by adding 2) when f -w and -k are present.  When used together -k and -w add two fields to the beginning of each row.  Implies --csv.",
    )
    csv_args.add_argument(
        "--sep",
        default=None,
        metavar="SEP",
        help="File is a csv deliminated by the specified character.  \\t specifies a tab character.  Default is any blank space.  Implies --csv.",
    )
    csv_args.add_argument(
        "--header",
        action="store_true",
        help="Skip the first line of the csv file.  The header is removed from the output unless -k is also specified.  Implies --csv.",
    )
    args = process_args(parser.parse_args())

    data = CommonArgs(
        args.infile,
        args.exclude,
        args.min,
        args.max,
        args.chars,
        args.required,
        args.lower,
        args.sort,
        args.shuffle,
        args.limit,
    )

    if args.csv:
        words = filter_words_csv(
            data, args.sortby, args.sep, args.field, args.keepfields, args.weight
        )
    else:
        words = filter_words_list(data)

    write_words(words, args.outfile)
    args.infile.close()
    args.outfile.close()
    if args.exclude is not None:
        args.exclude.close()


if __name__ == "__main__":
    main()
