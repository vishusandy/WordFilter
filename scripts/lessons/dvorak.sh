#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/../" || exit 1
# shellcheck disable=SC1091
. "../scripts/common.sh"
cd "../" || exit 1

dvorak="dvorak/"

# homerow basic
run --chars aoeuhtns \
    -w aoeuhtns \
    "${DATA_DIR}${dvorak}homerow_basic.csv" \
    "lesson_1_"
# --exclude "$(pre "${hrb%\.*}.txt" "$rem_prefix")" \

# homerow plus middle
run --chars aoeuhtnsid \
    --require id \
    -w aoeuhtn \
    -w id \
    "${DATA_DIR}${dvorak}homerow_middle.csv" \
    "lesson_2_"

# toprow basic
run --chars "aoeuhtnsid'pgcrl" \
    --require "'pgcrl" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    "${DATA_DIR}${dvorak}toprow_basic.csv" \
    "lesson_3_"

# toprow plus middle
run --chars "aoeuhtnsid'pgcrlyf" \
    --require "yf" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    -w "yf" \
    "${DATA_DIR}${dvorak}toprow_middle.csv" \
    "lesson_4_"

# bottom row
run --chars "aoeuhtnsid'pgcrlyfqjkmwvz" \
    --require "qjkbmwv" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    -w "yf" \
    -w "qjkmwvz" \
    "${DATA_DIR}${dvorak}bottomrow_basic.csv" \
    "lesson_5_"

# bottom rov plus middle
run --chars "aoeuhtnsid'pgcrlyfqjkmwvzxb" \
    --require "xb" \
    -w aoeuhtn \
    -w id \
    -w "'pgcrl" \
    -w "yf" \
    -w "qjkmwvz" \
    -w "xb" \
    "${DATA_DIR}${dvorak}bottomrow_middle.csv" \
    "lesson_6_"
