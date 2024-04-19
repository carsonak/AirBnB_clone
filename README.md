# AIRBNB CLONE

This is a clone of the AirBnb app.

## The Console

The console can be activated by typing the absolute or relative path to the
file [console.py](./console.py).

`./console.py`

It can also receive commands via a pipeline in a non-interactive way:

`echo "help create" | ./console.py`

In interactive mode, the console can be exited by pressing the keyboard
interrupt key, *ctrl+C*, the EOF key, *ctrl+D*, or by typing in the command
[`quit`](#quit).

### Commands

In interactive mode the console will display the prompt **`(hbnb)`** and wait
for input. There are a few commands that can be used described belowed.

#### quit

Exits the console, takes in no arguments.

#### help \[command\]

Prints out some text on how to use the console or specified command.

#### create \<classname>

#### show \<classname> \<id>

#### destroy \<classname> \<id>

#### all

#### update
