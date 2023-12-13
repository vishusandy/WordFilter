#!/usr/bin/env bash

# requires hunspell-devel package

dict="/usr/share/hunspell/en_US"
out="data/hunspell.txt"

unmunch "{$dict}.dic" "{$dict}.aff" >"$out"
