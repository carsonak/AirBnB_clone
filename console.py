#!/usr/bin/python3
"""Module for console."""

import cmd
import models
import typing

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Class for the HBNB shell."""

    prompt: str = "(hbnb) "
    __available_classes: typing.Dict[str, type] = {
        "BaseModel": BaseModel, "User": User, "Place": Place,
        "State": State, "City": City, "Amenity": Amenity, "Review": Review
    }

    def do_create(self, line: str) -> None:
        """Create and save a new class instance.

        Usage: create <ClassName>

        Arguments:
            <ClassName>: mandatory name of the class to be instantiated. The
            class should be one of BaseModel, User, Place, State, City,
            Amenity or Review.
        """  # noqa: D417
        if line:
            classname: str = line.split(maxsplit=1)[0]
            if classname in self.__available_classes:
                new_obj: BaseModel = self.__available_classes[classname]()
                new_obj.save()
                print(new_obj.id)
            else:
                print("** class doesn't exist **")

        else:
            print("** class name missing **")

    def do_show(self, line: str) -> None:
        """Display the specified instance.

        Usage: show <ClassName> <id>

        Arguments:
            <ClassName>: mandatory class name of the instance.
            <id>: mandatory unique id of the instance.
        """  # noqa: D417
        if not line:
            print("** class name missing **")
            return

        args: typing.List[str] = line.split(maxsplit=2)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        ins_key: str = ".".join(args[:2])
        if ins_key not in models.storage.all():
            print("** no instance found **")
            return

        print(models.storage.all()[ins_key])

    def do_destroy(self, line: str) -> None:
        """Delete the specified instance.

        Usage: destroy <ClassName> <id>

        Arguments:
            <ClassName>: mandatory class name of the instance.
            <id>: mandatory unique id of the instance.
        """  # noqa: D417
        if not line:
            print("** class name missing **")
            return

        args: typing.List[str] = line.split(maxsplit=2)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        ins_key: str = ".".join(args[:2])
        try:
            models.storage.all().pop(ins_key)
            models.storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, line: str) -> None:
        """Print a list of all objects or just of the specified class.

        Usage: all [ClassName]

        Arguments:
            [ClassName]: optional class name of the instances to be printed.
        """  # noqa: D417
        classname: str = line.split(maxsplit=1)[0] if line else ""

        if classname and classname not in self.__available_classes:
            print("** class doesn't exist **")
            return

        instances_list: typing.List[str] = []
        all_instances: typing.Dict[str, BaseModel] = models.storage.all()
        for key in all_instances:
            if classname:
                if key.startswith(classname):
                    instances_list.append(str(all_instances[key]))
            else:
                instances_list.append(str(all_instances[key]))
        else:
            print(instances_list)

    def do_update(self, line: str) -> None:
        """Update an existing instance's attribute.

        Usage: update <class name> <id> <attribute name> '<attribute value>'

        Arguments:
            <classname>: mandatory class name of the instance.
            <id>: mandatory id of the instance.
            <attribute name>: mandatory name of the attribute to be updated.
            <attribute value>: a string with the new value of the attribute.
        """  # noqa: D417
        if not line:
            print("** class name missing **")
            return

        args: typing.List[str] = line.split(maxsplit=4)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        ins_key: str = ".".join(args[:2])
        if ins_key not in models.storage.all():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attr_name: str = args[2]
        if len(args) < 4:
            print("** value missing **")
            return

        value: str = args[3]
        instance: BaseModel = models.storage.all()[ins_key]
        if hasattr(instance, attr_name):
            attr_type: type = type(getattr(instance, attr_name))
            setattr(instance, attr_name, attr_type(value))
        else:
            setattr(instance, attr_name, value)

        instance.save()

    def emptyline(self) -> bool:
        """Ignore empty lines."""
        return False

    def do_EOF(self, line: str) -> bool:  # noqa: N802
        """Exit the console."""
        print()
        return True

    def do_quit(self, line: str) -> bool:
        """Exit the console.

        Usage: quit
        """
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
