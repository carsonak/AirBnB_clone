#!/usr/bin/python3
"""Module for console."""

import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Class for the HBNB shell."""

    prompt: str = "(hbnb) "
    __available_classes: tuple[str, ...] = (
        "BaseModel", "User", "Place", "State", "City", "Amenity", "Review")

    def do_create(self, line: str) -> None:
        """create <ClassName>: Creates and saves a new BaseModel instance.

        Arguments:
            <ClassName>: mandatory name of the class to be instantiated.
            Should be one of: BaseModel, .
        """
        if line:
            args: list[str] = line.split(maxsplit=1)
            if args[0] in self.__available_classes:
                new_obj: BaseModel = globals()[args[0]]()
                new_obj.save()
                print(new_obj.id)
            else:
                print("** class doesn't exist **")

        else:
            print("** class name missing **")

    def do_show(self, line: str) -> None:
        """show <ClassName> <id>: Displays the specified instance.

        Arguments:
            <ClassName>: mandatory class name of the instance.
            <id>: mandatory unique id of the instance.
        """
        if not line:
            print("** class name missing **")
            return

        args: list[str] = line.split(maxsplit=2)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_key: str = ".".join(args[:2])
        if instance_key not in models.storage.__objects:
            print("** instance id missing **")
            return

        print(models.storage.__objects[instance_key])

    def do_destroy(self, line: str) -> None:
        """destroy <ClassName> <id>: Deletes the specified instance.

        Arguments:
            <ClassName>: mandatory class name of the instance.
            <id>: mandatory unique id of the instance.
        """
        if not line:
            print("** class name missing **")
            return

        args: list[str] = line.split(maxsplit=2)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_key: str = ".".join(args[:2])
        try:
            del models.storage.__objects[instance_key]
            models.storage.__objects.pop(instance_key)
            models.storage.save()
        except KeyError:
            print("** instance id missing **")

    def do_all(self, line: str) -> None:
        """all [ClassName]: prints list of all objects or just of the specified class.

        Arguments:
            [ClassName]: optional class name of the instances to be printed.
        """
        classname: str = line.split(maxsplit=1)[0] if line else ""

        if classname and classname not in self.__available_classes:
            print("** class doesn't exist **")
            return

        instances_list: list[str] = []
        all_instances: dict[str, BaseModel] = models.storage.all()
        for key in all_instances:
            if classname:
                if key.startswith(classname):
                    instances_list.append(str(all_instances[key]))
            else:
                instances_list.append(str(all_instances[key]))
        else:
            print(instances_list)

    def do_update(self, line: str) -> None:
        """update <class name> <id> <attribute name> '<attribute value>': updates an instance's attribute.

        Arguments:
            <classname>: compulsory class name of the instance.
            <id>: compulsory id of the instance.
            <attribute name>: compulsory name of the attribute to be updated.
            <attribute value>: the new value of the attribute.
        """
        if not line:
            print("** class name missing **")
            return

        args: list[str] = line.split(maxsplit=2)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_key: str = ".".join(args[:2])
        if instance_key not in models.storage.__objects:
            print("** instance id missing **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return
        elif len(args) < 4:
            print("** value missing **")
            return

        ins: BaseModel = models.storage.__objects[instance_key]
        setattr(ins, args[2], args[3])
        ins.save()

    def emptyline(self) -> bool:
        """Ignore emppty lines."""
        return False

    def do_EOF(self, line: str) -> bool:
        """Exit from the shell."""
        print()
        return True

    def do_quit(self, line: str) -> bool:
        """quit: Exits from the shell."""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
