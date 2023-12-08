#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

quit() {
    echo "Could not cd to project directory" >&2
    exit 1
}
if [ "$SCRIPT_DIR" != "$PWD" ]; then
    cd "$SCRIPT_DIR" || quit
fi
proj=$(basename "${SCRIPT_DIR}")
python3 -m src."$proj".filter "$@"

# file="src/word_filter/filter.py"
# python "$SCRIPT_DIR/$file" "$@"

# Dvorak homerow basic
# ./run.sh -c 'aoeuhtns' -m 4 -x 10 --csv --header /ares/docs/data/wordlists/unigram_freq.csv dvorak_homerow_basic.txt
# ./run.sh -c 'aoeuidhtns' -m 4 -x 10 --csv --header /ares/docs/data/wordlists/unigram_freq.csv dvorak_homerow_full.txt
