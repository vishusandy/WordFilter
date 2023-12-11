import argparse
import io
from typing import Any


def prepare(text: io.TextIOWrapper | str, sort: bool = False):
    if isinstance(text, str):
        arr = [l.strip() for l in text.splitlines() if l.strip() != ""]
    else:
        arr = [l.strip() for l in text.readlines() if l.strip() != ""]

    if sort:
        arr.sort()

    return arr


def add_remove(
    exclude_list: io.TextIOWrapper | str | None,
    include_list: io.TextIOWrapper | str | None,
    words: list[Any],
) -> list[Any]:
    if exclude_list is not None:
        return remove(exclude_list, words)
    if include_list is not None:
        return only(include_list, words)

    if exclude_list is not None and include_list is not None:
        output: list[Any] = []
        include = prepare(include_list)
        exclude = prepare(exclude_list)

        for word in words:
            if word not in exclude and word in include:
                output.append(word)

        return output

    return words


def add_remove_by(
    exclude_list: io.TextIOWrapper | str | None,
    include_list: io.TextIOWrapper | str | None,
    words: list[list[Any]],
    field: int,
) -> list[list[Any]]:
    if exclude_list is not None:
        return remove_by(exclude_list, words, field)
    if include_list is not None:
        return only_by(include_list, words, field)

    if exclude_list is not None and include_list is not None:
        output: list[list[Any]] = []
        include = prepare(include_list)
        exclude = prepare(exclude_list)

        for fields in words:
            word = fields[field]
            if word not in exclude and word in include:
                output.append(fields)

        return output

    return words


def only(
    include_list: io.TextIOWrapper | str,
    words: list[Any],
) -> list[Any]:
    output: list[Any] = []
    include = set(prepare(include_list))

    for word in words:
        if word in include:
            output.append(word)

    return output


def only_by(
    include_list: io.TextIOWrapper | str, words: list[list[Any]], field: int
) -> list[list[Any]]:
    output: list[list[Any]] = []
    include = set(prepare(include_list))

    for fields in words:
        word = fields[field]
        if word in include:
            output.append(fields)

    return output


def remove(
    exclude_list: io.TextIOWrapper | str,
    words: list[Any],
) -> list[Any]:
    output: list[Any] = []
    exclude = set(prepare(exclude_list))

    for word in words:
        if word not in exclude:
            output.append(word)

    return output


def remove_by(
    exclude_list: io.TextIOWrapper | str,
    words: list[list[Any]],
    field: int,
) -> list[list[Any]]:
    output: list[list[Any]] = []
    exclude = set(prepare(exclude_list))

    for fields in words:
        word = fields[field]
        if word not in exclude:
            output.append(fields)

    return output
