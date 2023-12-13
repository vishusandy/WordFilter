#!/usr/bin/env bash

# Requires the hunspell-devel package

dict="/usr/share/hunspell/en_US"
out="data/hunspell.txt"

unmunch "{$dict}.dic" "{$dict}.aff" | grep -E "^[a-z']+$" >"$out"
