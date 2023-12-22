#!/usr/bin/env bash

# printf "%s\n\n" "$(</dev/stdin)"

printf "[\n"

prev=""
while IFS=$'\n' read -r line; do
    if [ "$line" = "" ]; then continue; fi
    if [ "$prev" != "" ]; then echo "$prev,"; fi
    prev="$(printf "\t\"%s\"\n" "$line")"
done
echo "$prev"

printf "]"
