#!/usr/bin/python3
"""Module for console."""

import cmd
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Class for the HBNB shell."""

    prompt = '(hbnb) '
    __available_classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place, 'State': State,
        'City': City, 'Amenity': Amenity, 'Review': Review
    }

    def do_create(self, line):
        """Create and save a new class instance.

        Usage: create <ClassName>

        Arguments:
            <ClassName>: mandatory name of the class to be instantiated. The
            class should be one of BaseModel, User, Place, State, City,
            Amenity or Review.
        """
        if line:
            classname = line.split(maxsplit=1)[0]
            if classname in self.__available_classes:
                new_obj = self.__available_classes[classname]()
                new_obj.save()
                print(new_obj.id)
            else:
                print("** class doesn't exist **")
        else:
            print('** class name missing **')

    def do_show(self, line):
        """Display the specified instance.

        Usage: show <ClassName> <id>

        Arguments:
            <ClassName>: mandatory class name of the instance.
            <id>: mandatory unique id of the instance.
        """
        if not line:
            print('** class name missing **')
            return

        args = line.split(maxsplit=2)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        ins_key = '.'.join(args[:2])
        if ins_key not in models.storage._FileStorage__objects:
            print('** instance id missing **')
            return

        print(models.storage._FileStorage__objects[ins_key])

    def do_destroy(self, line):
        """Delete the specified instance.

        Usage: destroy <ClassName> <id>

        Arguments:
            <ClassName>: mandatory class name of the instance.
            <id>: mandatory unique id of the instance.
        """
        if not line:
            print('** class name missing **')
            return

        args = line.split(maxsplit=2)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        ins_key = '.'.join(args[:2])
        try:
            models.storage._FileStorage__objects.pop(ins_key)
            models.storage.save()
        except KeyError:
            print('** no instance found **')

    def do_all(self, line):
        """Print a list of all objects or just of the specified class.

        Usage: all [ClassName]

        Arguments:
            [ClassName]: optional class name of the instances to be printed.
        """
        classname = line.split(maxsplit=1)[0] if line else ''
        if classname and classname not in self.__available_classes:
            print("** class doesn't exist **")
            return

        instances_list = []
        all_instances = models.storage.all()
        for key in all_instances:
            if classname:
                if key.startswith(classname):
                    instances_list.append(str(all_instances[key]))
            else:
                instances_list.append(str(all_instances[key]))
        else:
            print(instances_list)

    def do_update(self, line):
        """Update an existing instance's attribute.

        Usage: update <class name> <id> <attribute name> '<attribute value>'

        Arguments:
            <classname>: mandatory class name of the instance.
            <id>: mandatory id of the instance.
            <attribute name>: mandatory name of the attribute to be updated.
            <attribute value>: a string with the new value of the attribute.
        """
        if not line:
            print('** class name missing **')
            return

        args = line.split(maxsplit=4)
        if args[0] not in self.__available_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        ins_key = '.'.join(args[:2])
        if ins_key not in models.storage._FileStorage__objects:
            print('** instance id missing **')
            return

        if len(args) < 3:
            print('** attribute name missing **')
            return

        elif len(args) < 4:
            print('** value missing **')
            return

        ins = models.storage._FileStorage__objects[ins_key]
        if args[2] in dir(ins):
            attr_type = type(getattr(ins, args[2]))
            setattr(ins, args[2], attr_type(args[3]))
            ins.save()
        else:
            print(f"** {args[0]} does not contain attribute '{args[2]}' **")

    def emptyline(self):
        """Ignore empty lines."""
        return False

    def do_EOF(self, line):
        """Exit the console."""
        print()
        return True

    def do_quit(self, line):
        """Exit the console.

        Usage: quit
        """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
