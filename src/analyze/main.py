import argparse
import io
import sys
from collections import defaultdict


class Freq:
    # freq of each character
    cf: dict[str, int] = defaultdict(int)
    # how many words it appears in
    w: dict[str, int] = defaultdict(int)
    words: int = 0
    chars: int = 0

    def print(self):
        print("Character frequencies:")
        for k, v in map(lambda k: (k, self.cf.get(k, 0)), sorted(self.cf)):
            # print(f"\t{k}={v} {v/self.chars}%")
            print("\t{}={} {:06.2%}".format(k, v, v / self.chars))

        print("\nOccurrences in words:")
        for k, v in map(lambda k: (k, self.w.get(k, 0)), sorted(self.w)):
            print("\t{}={} {:06.2%}".format(k, v, v / self.words))

        print(f"\nwords: {self.words}")
        print(f"chars: {self.chars}")

    def process(self, file: io.TextIOWrapper, header: bool):
        if isinstance(file, str):
            file = open(file, "rt")
        if header:
            file.readline()

        for word in file.readlines():
            word = word.strip()
            char_set: set[str] = set()
            chars = 0
            for c in word:
                self.cf[c] += 1
                char_set.add(c)
                chars += 1

            self.chars += chars
            self.words += 1
            for c in char_set:
                self.w[c] += 1
            char_set = set()


def main():
    # print(sys.argv)

    parser = argparse.ArgumentParser(
        description="Analyze letter frequencies in the specified file"
    )
    parser.add_argument(
        "files",
        type=argparse.FileType("rt"),
        default=sys.stdin,
        help="File to analyze",
        nargs="*",
    )
    parser.add_argument(
        "--header", action="store_true", help="skip first line in the file"
    )

    args = parser.parse_args()
    if not isinstance(args.files, list):
        args.files = [args.files]

    freq = Freq()
    for f in args.files:
        freq.process(f, args.header)

    freq.print()


if __name__ == "__main__":
    main()
