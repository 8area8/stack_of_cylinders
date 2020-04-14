"""Screen module.

Handle the screen.
"""
from typing import List

from termcolor import cprint, colored

from tanks.config import MAX_ITEMS
from tanks.tank import Tank

Tanks = List[Tank]


class Screen:
    """Display the game.

    Attributes:
        tanks (Tanks): the tank list.
    """

    def __init__(self, tanks: Tanks) -> None:
        """Initialize the tanks."""
        self.tanks: Tanks = tanks

    def display(self) -> List[str]:
        """Display the game.

        Returns:
            Dict[int, str]: the possible commands.
        """
        print()
        self.print_tanks()
        print()
        commands = self.print_commands()
        return commands

    def print_tanks(self) -> None:
        """Print the tanks."""
        last_to_first = range(MAX_ITEMS - 1, -1, -1)
        for line in last_to_first:
            for tank in self.tanks:
                try:
                    cprint(tank[line], "cyan", end="")
                except IndexError:
                    print(".", end="")
                print("  ", end="")
            print()

    def print_commands(self) -> List[str]:
        """Print the possible commands.

        Returns:
            List[str]: the possible commands.
        """
        commands = []
        cprint("COMMANDS", "red")
        cprint("--------", "red")
        for index, tank in enumerate(self.tanks):
            for direction in ("left", "right"):
                inner_tank = getattr(tank, direction)

                if tank and inner_tank is not None and inner_tank.can_add(tank[-1]):
                    cprint(self.print_possible_command(len(commands), index, direction))
                    commands.append(f"{index} {direction}")

        cprint("\nType your command:", "red", end=" ")
        return commands

    def print_possible_command(
        self, command_number: int, index: int, direction: str
    ) -> str:
        """Print the possible command.

        Args:
            command_number (int): the command number.
            index (int): the tank index.
            direction (str): the given direction.

        Returns:
            str: the colored informations.
        """
        pcommand = colored(str(command_number), "red")
        ptank = colored(f"tank {index + 1}", "cyan")
        pdirection = colored(direction, "cyan")
        return f"{pcommand}: {ptank} moove item to {pdirection}"
