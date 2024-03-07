#!/usr/bin/env bash

LANGUAGE=${LANGUAGE:-"en_US"}
HUNSPELL_PATH=${HUNSPELL_PATH:-"/usr/share/hunspell/"}
HUNSPELL_WORDLIST=${HUNSPELL_WORDLIST:-"data/hunspell.txt"}

# create list of unique words from hunspell dictionary if it does not exist
if [ ! -f "../$HUNSPELL_WORDLIST" ]; then
    unmunch "${HUNSPELL_PATH}${LANGUAGE}.dic" "${HUNSPELL_PATH}${LANGUAGE}.aff" 2>/dev/null | grep -E "^[a-z']+$" >"../$HUNSPELL_WORDLIST"
fi

# DEFAULT RUN VALUES
LIMIT=${LIMIT:-"2000"}
MIN=${MIN:-"4"}
MAX=${MAX:-"12"}

# DEFAULT SCRIPT VALUES
CREATE_TXT=${CREATE_TXT:-true}
CREATE_JSON=${CREATE_JSON:-true}
ANALYZE=${ANALYZE:-true}
DATA_DIR=${DATA_DIR:-"data/"}
WORDLIST=${WORDLIST:-"${DATA_DIR}unigram_freq.csv"}
DICT_GOOD=${DICT_GOOD:-"${HUNSPELL_WORDLIST}"}
DICT_BAD=${DICT_BAD:-"${DATA_DIR}unigram_freq_bad.txt"}

# prepend a string $2 to filename found in $1 (which may be a full path)
function prepend() {
    local add="${2}"
    local base
    base="$(basename "$1")"
    local lenb="${#base}"
    local lenf="${#1}"
    local lenp=$((lenf - lenb))
    echo "${1:0:lenp}$add$base"
}

# usage: run <args...> <filename> <lesson_prefix>
function run() {
    local last=$(($# - 1))
    local sec=$(($# - 2))
    local pre=${!#}
    local args=${*:1:$sec}
    local file=${!last}
    local base="${file%\.*}"
    local prefixed
    prefixed="$(prepend "${file}" "${pre}")"

    # shellcheck disable=SC2048,SC2086
    ./run.sh \
        -m "$MIN" \
        -M "$MAX" \
        -n "$LIMIT" \
        --sortby 3 \
        --rev \
        --header \
        --keep \
        --include "$DICT_GOOD" \
        --exclude "$DICT_BAD" \
        ${args[*]} \
        "$WORDLIST" \
        "$prefixed"

    if [ "$CREATE_TXT" = true ]; then
        ./run.sh --header -f 2 "$prefixed" | printf "%s\n" "$(</dev/stdin)" >"$(prepend "${base}.txt" "$pre")"
    fi
    if [ "$CREATE_JSON" = true ]; then
        ./run.sh --header -f 2 "$prefixed" | printf "%s\n" "$(</dev/stdin)" | ./scripts/misc/json_list.sh >"$(prepend "${base}.json" "$pre")"
    fi
    if [ "$ANALYZE" = true ]; then
        local a
        a="$(prepend "${file}" "analysis_$pre")"
        ./run.sh --header -f 2 "$prefixed" | python3 -m src.analyze.main >"${a%\.*}.txt"
    fi
}
