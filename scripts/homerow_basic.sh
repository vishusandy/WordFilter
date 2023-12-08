#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

run="$(realpath "$SCRIPT_DIR"/../filter.sh)"
wordlist="$(realpath "$SCRIPT_DIR"/../data/unigram_freq.csv)"
output="$(realpath "$SCRIPT_DIR"/../data/dvorak/dvorak_homerow_basic.txt)"
"$run" -c 'aoeuhtns' -m 4 -M 10 --csv -k --header "$wordlist" "$output"
# "$run" -c 'aoeuhtns' -m 4 -M 10 --csv --header "$wordlist" "$output"
# ../run.sh -c 'aoeuidhtns' -m 4 -x 10 --csv --header /ares/docs/data/wordlists/unigram_freq.csv dvorak_homerow_full.txt
