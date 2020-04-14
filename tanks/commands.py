"""Commands module."""

from typing import List

from termcolor import colored

from tanks import Tank


Tanks = List[Tank]
Commands = List[str]


class CommandHandler:
    """Command class.

    Ask for a command then resolve the commands.

    Attributes:
        tanks (Tanks): the tank list.
    """

    def __init__(self, tanks: Tanks) -> None:
        """Initialize the tanks."""
        self.tanks = tanks

    def wait_for(self, commands: Commands) -> None:
        """Ask for a command.

        Args:
            commands (List[str]): the possible commands.
        """
        message = ""
        is_good_input = False
        command = ""
        tank_index = ""
        direction = ""
        directives = ""
        tank = None

        while not is_good_input:
            command = input(message)
            try:
                directives = commands[int(command)]
                tank_index, direction = directives.split()
                is_good_input = True
            except IndexError:
                values = ", ".join([str(num) for num in range(len(commands))])
                error = f"\nWrong value ! Possible values are: {values}."
            except ValueError:
                error = "\nYour command is not a digit !"
            base_message = "Type your command: "
            message = f"{colored(error, 'yellow')}\n{colored(base_message, 'red')}"

        tank = self.tanks[int(tank_index)]
        tank.move_to_(direction)
