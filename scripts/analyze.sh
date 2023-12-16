#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR/../" || exit 1

data="data/"
dvorak="dvorak/"

analyze() {
    ./run.sh --header -f 2 "$data$dvorak$1.csv" | python3 -m src.analyze.main >"$data/dvorak/analysis_$1.txt"
}

analyze "lesson_1_homerow_basic"
analyze "lesson_2_homerow_middle"
analyze "lesson_3_toprow_basic"
analyze "lesson_4_toprow_middle"
analyze "lesson_5_bottomrow_basic"
analyze "lesson_6_bottomrow_middle"
