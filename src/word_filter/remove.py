import argparse
import io


def remove(
    exclude_file: io.TextIOWrapper,
    wordlist_file: io.TextIOWrapper,
):
    exclude = [l.strip() for l in exclude_file.readlines() if l.strip() != ""]
    exclude.sort()

    words = [l.strip() for l in wordlist_file.readlines() if l.strip() != ""]
    words.sort()

    word_len = len(words)
    exc_len = len(exclude)

    iw = 0
    ie = 0

    while iw < word_len and ie < exc_len:
        w = words[iw]
        e = exclude[ie]
        if w == e:
            words[iw] = ""
            iw += 1
            ie += 1
        if w < e or ie >= exc_len:
            iw += 1
            print(w)
        else:
            ie += 1
    while iw < word_len:
        print(words[iw])
        iw += 1


def main():
    parser = argparse.ArgumentParser(description="Filter words")
    parser.add_argument(
        "exclude",
        metavar="exclude_file",
        type=argparse.FileType("r"),
        help="Exclude list file",
    )
    parser.add_argument(
        "wordlist",
        metavar="wordlist_file",
        type=argparse.FileType("r"),
        help="Wordlist file",
    )

    args = parser.parse_args()

    remove(args.exclude, args.wordlist)


if __name__ == "__main__":
    main()
