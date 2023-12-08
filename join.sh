#!/usr/bin/env bash

cat "$1" "$2" | sort | uniq
