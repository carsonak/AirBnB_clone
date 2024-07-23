# AIRBNB CLONE

This is a clone of AirBnb.

## The Console

To use the console in interactive mode run the following command in a terminal.

`python3 console.py`

The prompt **`(hbnb)`** will be displayed on screen indicating that the console
is ready for input. There are several commands that can be used on the console
discussed below. To exit interactive mode type in the command `quit` or
press the keys *Ctrl+D* or *Ctrl+C*.

Commands can also be passed to the console via a pipeline which causes the
console to execute the commands passed and immediately exit therefore not
activating interactive mode.

`echo "help create" | python3 console.py`

| Command | Description |
| :----: | :--- |
| `all [ClassName]` | Prints the string representation of all instances. The optional argument `ClassName` can be used to limit the output to only instances of a specific class. |
| `create <ClassName>` | Creates and saves a new instance of `ClassName` and prints out its uuid.  |
| `destroy <ClassName> <id>` | Deletes an instance based on the class name and id. |
| `help [command]` | Prints some help text. If a command is specified, prints help text of that particular command. |
| `show <ClassName> <id>` | Prints the string representation of an instance based on the class name and id. |
| `update <class name> <id> <attribute name> "<attribute value>"` | Updates an instance based on the class name and id by adding or updating an attribute. The command can only update a single instance and attribute at a time. Any `attribute value` containing spaces should be quoted. |
| `quit` | Exits the console. |
| `EOF` | Exits the console. |

For all the above commands with arguments, the sequence of the arguments is important. Only one command may be processed per line.

```bash
> python3 console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb)
(hbnb)
(hbnb) help create
Create and save a new class instance.

        Usage: create <ClassName>

        Arguments:
            <ClassName>: mandatory name of the class to be instantiated. The
            class should be one of BaseModel, User, Place, State, City,
            Amenity or Review.

(hbnb) create User
c7ee894f-bc2b-4929-a902-af7cdc931a72
(hbnb)
(hbnb) show User c7ee894f-bc2b-4929-a902-af7cdc931a72
[User] (c7ee894f-bc2b-4929-a902-af7cdc931a72) {'id': 'c7ee894f-bc2b-4929-a902-af7cdc931a72', 'created_at': datetime.datetime(2024, 7, 23, 2, 58, 14, 277665), 'updated_at': datetime.datetime(2024, 7, 23, 2, 58, 14, 278073)}
(hbnb)
(hbnb)
(hbnb) create City
fe9b4b10-d2ae-4104-9511-8ed7c1c74ccf
(hbnb)
(hbnb)
(hbnb) all
["[User] (c7ee894f-bc2b-4929-a902-af7cdc931a72) {'id': 'c7ee894f-bc2b-4929-a902-af7cdc931a72', 'created_at': datetime.datetime(2024, 7, 23, 2, 58, 14, 277665), 'updated_at': datetime.datetime(2024, 7, 23, 2, 58, 14, 278073)}", "[City] (fe9b4b10-d2ae-4104-9511-8ed7c1c74ccf) {'id': 'fe9b4b10-d2ae-4104-9511-8ed7c1c74ccf', 'created_at': datetime.datetime(2024, 7, 23, 2, 58, 51, 136132), 'updated_at': datetime.datetime(2024, 7, 23, 2, 58, 51, 136198)}"]
(hbnb)
(hbnb)
(hbnb) quit
>
```
