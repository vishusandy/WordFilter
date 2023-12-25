#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/../" || exit 1
# shellcheck disable=SC1091
. "../scripts/common.sh"
cd "../" || exit 1

path="dvorak/"

tier1=aoeuhtns
tier2=id
tier3="'pgcrl"
tier4=yf
tier5=qjkmwvz
tier6=xb

# homerow
run --chars "${tier1}" \
    -w "${tier1}" \
    "${DATA_DIR}${path}homerow_basic.csv" \
    "lesson_1_"

# homerow plus middle
run --chars "${tier1}${tier2}" \
    --require "${tier2}" \
    -w "${tier1}" \
    -w "${tier2}" \
    "${DATA_DIR}${path}homerow_middle.csv" \
    "lesson_2_"

# toprow
run --chars "${tier1}${tier2}${tier3}" \
    --require "${tier3}" \
    -w "${tier1}" \
    -w "${tier2}" \
    -w "${tier3}" \
    "${DATA_DIR}${path}toprow_basic.csv" \
    "lesson_3_"

# toprow plus middle
run --chars "${tier1}${tier2}${tier3}${tier4}" \
    --require "${tier4}" \
    -w "${tier1}" \
    -w "${tier2}" \
    -w "${tier3}" \
    -w "${tier4}" \
    "${DATA_DIR}${path}toprow_middle.csv" \
    "lesson_4_"

# bottom row
run --chars "${tier1}${tier2}${tier3}${tier4}${tier5}" \
    --require "${tier5}" \
    -w "${tier1}" \
    -w "${tier2}" \
    -w "${tier3}" \
    -w "${tier4}" \
    -w "${tier5}" \
    "${DATA_DIR}${path}bottomrow_basic.csv" \
    "lesson_5_"

# bottom row plus middle
run --chars "${tier1}${tier2}${tier3}${tier4}${tier5}${tier6}" \
    --require "${tier6}" \
    -w "${tier1}" \
    -w "${tier2}" \
    -w "${tier3}" \
    -w "${tier4}" \
    -w "${tier5}" \
    -w "${tier6}" \
    "${DATA_DIR}${path}bottomrow_middle.csv" \
    "lesson_6_"
