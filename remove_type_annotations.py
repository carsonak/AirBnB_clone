#!/usr/bin/python3
"""Module for remove_type_annotations."""

import regex
import os
import json


class RemoveAnnotations:
    """Class for RemoveAnnotations."""

    __annotations_pattern: str = r"""
    ## Match Type Annotations for Return Values ##
    (?P<returns>\ ->
        ## Recursive Matching Annonations ##
        # Triggered by a word and stopped by the absence of a '|' character.
        # Meaning this block will keep matching as long as this character
        # appears after the optional '[]' braces.
        # The negative look-ahead ensures that class calls within dicts aren't
        # matched, e.g {"user1": User("Joe")}
        (?P<recurse>\ [[:alpha:]]+(?![[:alpha:](])
            ## Recursively Match Square Braces ##
            # A '[' triggers the recursion and a '[' stops it.
            # The quantifier '+' ensures this is repeated indefinetly.
            # To prevent the recursion afromm matching infinitely, a ']'is our
            # base case where the recursion must end with it, this effectively
            # matches everything within the outer most brackets.
            # The quantifier '?' makes the braces optional.
            ((?P<braces>\[ ([^[\]]+ | (?P&braces))+ \])? | \ \|(?P&recurse)))) |
    ## Match Type Annotations for Variables and Function Parameters ##
    # Repeat same recursion.
    (?P<args_vars>:(?P&recurse))
    """
    __directives_pattern: str = r"""\#(?P<directives>\ type:\ \w+$)"""
    __imports_pattern: str = r"""
    (?P<imports>(import\ typing | from\ typing(\.\w+)*\ import\ \w+(,\ \w+)*$))
    """

    def __init__(self, py_files: str | tuple[str, ...] = (),
                 folders: str | tuple[str, ...] = (),
                 flags: int = 0) -> None:
        """Initialise instance attributes."""
        self.__pattern_object: regex.Pattern | None = None
        self.__folders_dict: dict[str, tuple[str, ...]] = {}
        self.py_files: str | tuple[str, ...] = py_files  # type: ignore
        self.folders: str | tuple[str, ...] = folders  # type: ignore
        self.flags: int = flags

    @property
    def flags(self) -> int:
        """Return current set flags."""
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
        """Check for .py file extensions and store the paths.

        Args:
            py_files [str | tuple[str, ...]]: It is either a path to a single
            python script or a tuple of multiple paths.
        """
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

        p_len: int = len(self.__py_files)
        if p_len:
            self.__folders_dict["00 unknown"] = self.__py_files
            print(f"Files in cache: {p_len}")

    @property
    def folders(self) -> tuple[str, ...]:
        """Return directories to be processed."""
        return self.__folders

    @folders.setter
    def folders(self, folders: str | tuple[str, ...]) -> None:
        """Extract Python files from directories and store the paths.

        Args:
            folders [str | tuple[str, ...]]: It is either a path to a single
            directory with python scripts or a tuple with multiple paths.
        """
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
        """Substitute repl whenever regex_str matches the text in the file."""
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
        """Return a dict of filenames and their list of matched strings."""
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
    i = RemoveAnnotations(folders=("models", "tests/test_models", "tests/test_models/test_engine"))
    i.sub()
    # with open("matched_groups.json", "w", encoding="utf-8") as file:
    #     json.dump(i.find_matches(), file, indent="\t")


if __name__ == "__main__":
    main()
