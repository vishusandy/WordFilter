
# Word Filter

Filters a list of words.  Intended to be used to generate word lists for typing tutors, but may be useful for other purposes.

## Features
- Filters
    - min and max word lengths
    - required characters - filters out words that do not have any of the required characters
    - exclude file - filters out any words found in this file
    - include file - only include words found in this file
- Sorting
    - tiered weights - useful for keyboard tutors to generate lessons that build on previous lessons but prioritize characters in higher tiers
    - ascending and descending alphabetical sorting
    - random shuffling
    - sort by CSV column
- CSV
    - supports automatic detection of csv files (with or without headers)
    - sort by a specified column (numbers and text supported)
    - allows keeping or discarding csv columns in final output (for when you want to sort by a column but not include it in the output)

## Install

```sh
git clone https://github.com/vishusandy/WordFilter.git
cd WordFilter
./install.sh

```

## Usage

```sh
# Basic usage
./run.sh [inputfile] [outputfile]

# Help
./run.sh --help
```

For examples of advanced usage, like using tiered weights, see the [scripts/lessons](https://github.com/vishusandy/WordFilter/tree/main/scripts/lessons) directory.


## License

[Apache-2.0](https://spdx.dev/ids/)

<!-- SPDX-License-Identifier: Apache-2.0 -->
