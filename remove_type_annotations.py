#!/usr/bin/python3
"""Module for remove_type_annotations."""

import regex
import os
import json


class RemoveAnnotations:
    """Class for RemoveAnnotations."""

    __annotations_pattern: str = r"""
    (?P<returns>\ -> # return values annotations
        (?P<recurse>\ [[:alpha:]]+ # recursive pattern matching
            ((?P<braces>\[ ([^[\]]+ | (?P&braces))+ \])? | # recursive braces
        \ \|(?P&recurse)))) |
    (?P<args_vars>:(?P&recurse)) # variables and function parameter annotations
    """
    __directives_pattern: str = r"""\#(?P<directives>\ type:\ \w+$)"""
    __imports_pattern: str = r"""
    (?P<imports>(import\ typing | from\ typing(\.\w+)*\ import\ \w+(,\ \w+)*$))
    """

    def __init__(self, py_files: str | tuple[str, ...] = (),
                 folders: str | tuple[str, ...] = (),
                 flags: int = 0) -> None:
        """Initialise some instance attributes."""
        self.__pattern_object: regex.Pattern | None = None
        self.__folders_dict: dict[str, tuple[str, ...]] = {}
        self.py_files: str | tuple[str, ...] = py_files  # type: ignore
        self.folders: str | tuple[str, ...] = folders  # type: ignore
        self.flags: int = flags

    @property
    def flags(self) -> int:
        """Return self.flags."""
        return self.__flags

    @flags.setter
    def flags(self, val: int) -> None:
        """Set flags."""
        if type(val) is not int:
            raise TypeError("flags must be an int")

        self.__flags: int = val

    @property
    def py_files(self) -> tuple[str, ...]:
        """Return files to be processed."""
        return self.__py_files

    @py_files.setter
    def py_files(self, py_files: str | tuple[str, ...]) -> None:
        """Check file extensions and store paths."""
        if type(py_files) is str:
            if os.path.splitext(py_files)[1] == ".py":
                self.__py_files = tuple([py_files])
            else:
                raise ValueError("filename must end with .py")
        elif type(py_files) is tuple:
            file_list: list[str] = []
            for f in py_files:
                if type(f) is str and os.path.splitext(f)[1] == ".py":
                    file_list.append(f)
            else:
                self.__py_files = tuple(file_list)
        else:
            raise TypeError("py_file must be a string or a tuple of strings")

        self.__folders_dict["00 unknown"] = self.__py_files
        print(f"Files in cache: {len(self.__py_files)}")

    @property
    def folders(self) -> tuple[str, ...]:
        """Return directories to be processed."""
        return self.__folders

    @folders.setter
    def folders(self, folders: str | tuple[str, ...]) -> None:
        """Extract Python files from directories and store the paths."""
        if type(folders) is str:
            self.__folders = tuple([folders])
        elif type(folders) is tuple:
            self.__folders = tuple([f for f in folders if type(f) is str])
        else:
            raise TypeError("folders must be a string or a tuple of strings.")

        for dirname in self.__folders:
            file_list: list[str] = []
            with os.scandir(dirname) as folder:
                for entry in folder:
                    ext: str = os.path.splitext(entry.path)[1]
                    if entry.is_file() and ext == ".py":
                        file_list.append(entry.path)
                else:
                    self.__folders_dict[dirname] = tuple(file_list)
                    self.py_files = tuple([*self.py_files, *file_list])

        d_len: int = len(self.__folders_dict)
        if d_len > 1 or "00 unknown" not in self.__folders_dict:
            print("Discovered {} files in {} directories.".format(
                len(self.py_files), d_len))

    def sub(self, regex_str: str = "", repl: str = "", flags: int = 0) -> None:
        """Substitute repl wherever regex_str matches."""
        self.__pattern_object = self.compile(regex_str, flags)
        for filename in self.py_files:
            with open(filename, "r", encoding="utf-8") as file:
                contents: str = file.read()

            edited: str = self.__pattern_object.sub(repl, contents)
            if edited:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(edited)

    def compile(self, regex_str: str = "", flags: int = 0) -> regex.Pattern:
        """Compile a regex pattern."""
        if type(regex_str) is not str:
            raise TypeError("regex_str must be a string")

        if regex_str or not self.__pattern_object:
            if regex_str:
                compile_str: str = regex_str
                self.flags = flags
            else:
                compile_str = self.__annotations_pattern + r"|" +\
                    self.__directives_pattern + r"|" +\
                    self.__imports_pattern
                self.flags = int(regex.VERBOSE | flags)

            self.__pattern_object = regex.compile(
                compile_str, flags=self.flags)

        return self.__pattern_object

    def find_matches(self, regex_str: str = "", flags: int = 0) -> dict[str, list[str | list]]:
        """Return a dicti of filenames and their list of matched strings."""
        self.flags = flags
        self.__pattern_object = self.compile(regex_str, self.flags)
        file_matches: dict[str, list[str | list]] = {}
        for filename in self.py_files:
            with open(filename, "r", encoding="utf-8") as file:
                contents: str = file.read()

            file_matches[filename] = self.__pattern_object.findall(
                contents, overlapped=True)

        return file_matches

    def reset(self) -> None:
        """Reset all instance attributes."""
        self.flags = 0
        self.py_files = ()
        self.folders = ()
        self.__pattern_object = None
        self.__folders_dict = {}


def main() -> None:
    """Entry Point."""
    i = RemoveAnnotations(folders="models")
    i.compile()
    with open("matched_groups.json", "w", encoding="utf-8") as file:
        json.dump(i.find_matches(), file, indent="\t")


if __name__ == "__main__":
    main()
