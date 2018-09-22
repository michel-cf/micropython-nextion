# Nextion Lite Library

## Introduction
The lite does not have any meaning for which display you use. (Size and/or enhanced)

It is for the fact that this library only is a utility to make communication easier.
It's only an extension of the standard UART library. It provides a list of the most used commands,
a method to send commands and one to check for incoming data that then parses the response and calls a callback method you provide.

It doesn't know about your screen designs, id's or any logic you might have built into the screens.

## Usage

### Initialization

Import the library, and initialize for the UART you have connected your screen to. (Default = 1)
You can also provide the baud, but it has a default of 9600, which is the default for Nextion displays.

    import nextion
    n = nextion.Nextion(4)

### Executing a command:

Put the command as the first argument, and any values as next ones.

    n.send(nextion.COMMAND_VISIBLE, 'b0', 0)

You can also just write the text of the command. (Primarily useful for commands not included in the library)

    n.send('vis', 'b0', 0)

To set the text on a button:

    n.send('b0.txt="Test"')

