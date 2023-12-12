#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

cd "$SCRIPT_DIR/../" || exit 1
pwd
run="./run.sh"
wordlist="data/unigram_freq.csv"

hrb="data/dvorak/homerow_basic.txt"
hrm="data/dvorak/homerow_middle_full.txt"
# "$run" -c 'aoeuhtns' -m 4 -M 10 --csv -k --header "$wordlist" "$output"

# "./run.sh" -m 4 -M 12 --chars aoeuhtns --include concat.txt --exclude data/dvorak/homerow_basic_remove.txt --header data/unigram_freq.csv homerow_basic.txt

# "./run.sh" -m 4 -M 12 \
#     --chars aoeuhtns \
#     --header \
#     --include data/concat.txt \
#     --exclude data/dvorak/homerow_basic_remove.txt \
#     "$wordlist" "$hrb"

./run.sh -m 4 -M 12 \
    --chars aoeuhtnsid \
    --require id \
    --sortby 3 \
    --rev \
    --header \
    --include data/concat.txt \
    --exclude data/dvorak/homerow_basic_remove.txt \
    -w aoeuhtn -w id \
    "$wordlist" \
    "$hrm"
