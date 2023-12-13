import io
from typing import Any


def prepare(text: io.TextIOWrapper | str | None, sort: bool = False) -> set[str] | None:
    if text is None:
        return None
    if isinstance(text, str):
        arr = [l.strip() for l in text.splitlines() if l.strip() != ""]
    else:
        arr = [l.strip() for l in text.readlines() if l.strip() != ""]

    if sort:
        arr.sort()

    return set(arr)


def add_remove(
    exclude_list: io.TextIOWrapper | str | None,
    include_list: io.TextIOWrapper | str | None,
    words: list[Any],
) -> list[Any]:
    if exclude_list is None and include_list is None:
        return words

    output: list[Any] = []
    include = prepare(include_list)
    exclude = prepare(exclude_list)

    for word in words:
        if (exclude is None or word not in exclude) and (
            include is None or word in include
        ):
            output.append(word)

    return output


def add_remove_by(
    exclude_list: io.TextIOWrapper | str | None,
    include_list: io.TextIOWrapper | str | None,
    words: list[list[Any]],
    field: int,
) -> list[list[Any]]:
    if exclude_list is None and include_list is None:
        return words

    output: list[list[Any]] = []
    include = prepare(include_list)
    exclude = prepare(exclude_list)
    for fields in words:
        word = fields[field]
        if (exclude is None or word not in exclude) and (
            include is None or word in include
        ):
            output.append(fields)
    return output
