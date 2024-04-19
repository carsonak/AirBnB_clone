#!/usr/bin/python3
"""Module for console."""

import cmd


class HBNBCommand(cmd.Cmd):
    """Class for the HBNB console."""


if __name__ == '__main__':
    HBNBCommand().cmdloop()
