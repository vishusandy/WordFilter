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
if [ "$#" != 0 ]; then
    python3 -m src."$proj".main "$@"
else
    python3 -m src."$proj".main "--help"
fi
