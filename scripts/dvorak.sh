#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

cd "$SCRIPT_DIR/../" || exit 1
wordlist="data/unigram_freq.csv"

hrb="data/dvorak/homerow_basic.txt"
hrm="data/dvorak/homerow_middle.txt"

"./run.sh" -m 4 -M 12 \
    --chars aoeuhtns \
    --header \
    --include data/hunspell.txt \
    --exclude data/dvorak/homerow_basic_remove.txt \
    "$wordlist" \
    "$hrb"

./run.sh -m 4 -M 12 \
    --chars aoeuhtnsid \
    --require id \
    --sortby 3 \
    --rev \
    --header \
    --include data/hunspell.txt \
    --exclude data/dvorak/homerow_middle_remove.txt \
    -w aoeuhtn -w id \
    "$wordlist" \
    "$hrm"
