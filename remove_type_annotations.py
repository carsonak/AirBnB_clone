#!/usr/bin/python3
"""Module for remove_type_annotations."""

import regex


def remove_type_annotations(filename: str) -> None:
    """Find and remove type annotations in a python script."""
    annotations_pattern: str = r"""
    (?P<returns> -> # return values group
        (?P<recurse>\ \w+ # recursive annotation pattern
            ((?P<braces>\[ ([^[\]]+ | (?=braces))+ \]) # recursive '[]' pattern
        ? | \ \|(?=recurse))))
    : | \w+
    (?P<variables>:(?=recurse)) # repeat for variables and parameters
    (,\  | \) | \ =)
    """
    directives_pattern: str = r"""(?P<directives>\#\ type:\ ignore)"""
    imports_pattern: str = r"""
    (?P<imports>(import\ typing | from\ typing(\.\w+)*\ import\ \w+(,\ \w+)*$))
    """

    p_obj: regex.Pattern = regex.compile(r"(?x)" + annotations_pattern + r"|" +
                                         directives_pattern + r"|" + imports_pattern, 1)
    with open(filename, "r", encoding="utf-8") as file:
        contents: str = file.read()

    m_obj: regex.Match | None = p_obj.search(contents)
    if m_obj:
        m_obj.allcaptures()
    with open("temp.py", "w", encoding="utf-8") as file:
        file.write(contents)


if __name__ == "__main__":
    pass
