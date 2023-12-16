#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/../" || exit 1

data="data/"
dvorak="dvorak/"
wordlist="$data/unigram_freq.csv"

# output files
hrb="${data}${dvorak}homerow_basic.csv"
hrm="${data}${dvorak}homerow_middle.csv"
trb="${data}${dvorak}toprow_basic.csv"
trm="${data}${dvorak}toprow_middle.csv"
brb="${data}${dvorak}bottomrow_basic.csv"
brm="${data}${dvorak}bottomrow_middle.csv"

rem_prefix="remove_"

function pre() {
    local add="${2-$rem_prefix}"
    local base
    base="$(basename "$1")"
    local lenb="${#base}"
    local lenf="${#1}"
    local lenp=$((lenf - lenb))
    echo "${1:0:lenp}$add$base"
}

# rem_suffix=".remove"
# function mid() {
#     local name="${1%.*}"
#     local ext="${1##*.}"
#     if [ "$ext" != "" ]; then
#         ext=".$ext"
#     fi

#     echo "$name$rem_suffix$ext"
# }

function run() {
    "./run.sh" -m "4" -M "12" \
        --sortby 3 \
        --rev \
        -n 2000 \
        --header \
        --keep \
        --include data/hunspell.txt \
        "$@"
}

# homerow basic
run --chars aoeuhtns \
    -w aoeuhtns \
    --exclude "$(pre "${hrb%\.*}.txt")" \
    "$wordlist" \
    "$(pre "$hrb" "lesson_1_")"

# homerow plus middle
run --chars aoeuhtnsid \
    --require id \
    -w aoeuhtn \
    -w id \
    --exclude "$(pre "${hrm%\.*}.txt")" \
    "$wordlist" \
    "$(pre "$hrm" "lesson_2_")"

# toprow basic
run --chars "aoeuhtnsid'pgcrl" \
    --require "'pgcrl" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    "$wordlist" \
    "$(pre "$trb" "lesson_3_")"

# toprow plus middle
run --chars "aoeuhtnsid'pgcrlyf" \
    --require "yf" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    -w "yf" \
    "$wordlist" \
    "$(pre "$trm" "lesson_4_")"

# bottom row
run --chars "aoeuhtnsid'pgcrlyfqjkmwvz" \
    --require "qjkbmwv" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    -w "yf" \
    -w "qjkmwvz" \
    "$wordlist" \
    "$(pre "$brb" "lesson_5_")"

# bottom rov plus middle
run --chars "aoeuhtnsid'pgcrlyfqjkmwvzxb" \
    --require "xb" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    -w "yf" \
    -w "qjkmwvz" \
    -w "xb" \
    "$wordlist" \
    "$(pre "$brm" "lesson_6_")"
