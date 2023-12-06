#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

quit() {
    echo "Could not cd to project directory" >&2
    exit 1
}

if [ "$SCRIPT_DIR" != "$PWD" ]; then
    cd "$SCRIPT_DIR" || quit
fi

python -m unittest
