import argparse
import io


def remove(
    exclude_file: io.TextIOWrapper,
    words: list[str],
) -> list[str]:
    exclude = [l.strip() for l in exclude_file.readlines() if l.strip() != ""]
    exclude.sort()
    words.sort()

    output: list[str] = []
    word_len = len(words)
    exc_len = len(exclude)
    iw = 0
    ie = 0

    while iw < word_len and ie < exc_len:
        w = words[iw]
        e = exclude[ie]
        if w == e:
            iw += 1
            ie += 1
        if w < e or ie >= exc_len:
            output.append(words[iw])
            iw += 1
        else:
            ie += 1
    while iw < word_len:
        output.append(words[iw])
        iw += 1

    return output


def remove_by(
    exclude_file: io.TextIOWrapper,
    words: list[list[str]],
    field: int,
) -> list[list[str]]:
    exclude = [l.strip() for l in exclude_file.readlines() if l.strip() != ""]
    exclude.sort()
    words.sort(key=lambda w: w[field])

    output: list[list[str]] = []
    word_len = len(words)
    exc_len = len(exclude)
    iw = 0
    ie = 0

    while iw < word_len and ie < exc_len:
        w = words[iw][field]
        e = exclude[ie]
        if w == e:
            iw += 1
            ie += 1
        if w < e or ie >= exc_len:
            output.append(words[iw])
            iw += 1
        else:
            ie += 1
    while iw < word_len:
        output.append(words[iw])
        iw += 1

    return output


def remove_print(
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
            iw += 1
            ie += 1
        if w < e or ie >= exc_len:
            print(w)
            iw += 1
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

    remove_print(args.exclude, args.wordlist)


if __name__ == "__main__":
    main()
