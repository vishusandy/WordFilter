#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
file="src/word_filter/remove.py"

python "$SCRIPT_DIR/$file" "$@"
