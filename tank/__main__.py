"""Tank module."""

import logging
from typing import Optional, List, Dict

from termcolor import cprint, colored


# Constants

MAX_ITEMS = 4
MAX_TANKS = 3

LOGGER_LEVEL = logging.INFO
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOGGER_LEVEL)
CONSOLE = logging.StreamHandler()
LOGGER.addHandler(CONSOLE)


# Personal types

Tanks = List["Tank"]
Commands = Dict[int, str]


class Tank(list):
    """Tank class.

    Args:
        left (Tank, optional): the left linked tank.
        right (Tank, optional): the right linked tank.
    """

    def __init__(
        self, number: int, *args, **kwargs,
    ):
        """Initialize the tanks."""
        super().__init__(*args, **kwargs)
        self.left: Optional[Tank] = None
        self.right: Optional[Tank] = None
        self.number: int = number

    @property
    def is_full(self) -> bool:
        """Return True if you cannot add an item.

        Returns:
            bool: True if the tank is full, else False.
        """
        return len(self) == MAX_ITEMS

    def can_add(self, item: int) -> bool:
        """Return True if you can add the item.

        Args:
            item (int): the wanted item.

        Returns:
            bool: True if the item can be added, else False.
        """
        if not self:
            return True
        return item < self[-1] and not self.is_full

    def full_in(self, *items: int) -> None:
        """Append some items if they are integer and the tank is not full.

        Args:
            items (int): items to add.
        """
        for item in items:
            if not self.is_full and isinstance(item, int):
                self.add(item)

    def add(self, item: int):
        """Parent append method.

        Args:
            item (int): the integer to append.
        """
        super().append(item)

    def append(self, _):
        """Remove append method."""
        return None

    def move_to_(self, direction: str) -> bool:
        """Move the last item to the given direction.

        Remove the last item of the current tank. Give it the the linked tank.

        Args:
            direction (str): the wanted direction.

        Returns:
            bool: the result status.
        """
        inner_tank: Tank = getattr(self, direction)

        if inner_tank.can_add(self[-1]):
            inner_tank.add(self.pop())
            return True

        print(f"Wrong direction: {direction} - {inner_tank} - {self[-1]}")
        return False

    def __str__(self):
        """Return the representation of Tank."""
        return f"Tank-{self.number}-{super().__str__()}"


class Screen:
    """Display the game.

    Attributes:
        tanks (Tanks): the tank list.
    """

    def __init__(self, tanks: Tanks) -> None:
        """Initialize the tanks."""
        self.tanks = tanks

    def display(self) -> Commands:
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

    def print_commands(self) -> Commands:
        """Print the possible commands."""
        commands = {}
        command_number = 0
        cprint("COMMANDS", "red")
        cprint("--------", "red")
        for index, tank in enumerate(self.tanks):
            for direction in ("left", "right"):
                inner_tank = getattr(tank, direction)

                LOGGER.debug(self.print_commands_objects(tank, inner_tank, direction))

                if tank and inner_tank is not None and inner_tank.can_add(tank[-1]):
                    LOGGER.info(
                        self.print_possible_command(command_number, index, direction)
                    )
                    commands[command_number] = f"{index} {direction}"
                    command_number += 1

        cprint("\nType your command:", "red", end=" ")
        return commands

    def print_commands_objects(
        self, tank: Tank, inner: Optional[Tank], direction: str
    ) -> str:
        """Print the command objects.

        Args:
            tank (Tank): the tank object.
            inner (Tank): the inner tank object.
            direction (str): the given direction.

        Returns:
            str: the colored informations.
        """
        ptank = colored(f"tank {tank}", "red")
        pinner = colored(f"inner {direction} {inner}", "magenta")
        return f"{ptank} {pinner}"

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
        direction = colored(direction, "cyan")
        return f"{pcommand}: {ptank} moove item to {direction}"


class CommandHandler:
    """Command class.

    Ask for a command then resolve the commands.

    Attributes:
        tanks (Tanks): the tank list.
    """

    def __init__(self, tanks: Tanks) -> None:
        """Initialize the tanks."""
        self.tanks = tanks

    def ask(self, commands: Dict[int, str]) -> None:
        """Ask for a command.

        Args:
            commands (Dict[int, str]): the possible commands.
        """
        command = input()
        tank_index, direction = commands[int(command)].split()
        tank = self.tanks[int(tank_index)]
        tank.move_to_(direction)


def init_tanks() -> Tanks:
    """Initialize the tanks.

    Returns:
        List[Tank]: the tank list.
    """
    tanks: Tanks = []
    last: Optional[Tank] = None

    for number in range(MAX_TANKS):
        tank = Tank(number + 1)
        tanks.append(tank)
        if isinstance(last, Tank):
            last.right, tank.left = tank, last
        last = tank

    items = range(MAX_ITEMS, 0, -1)
    tanks[0].full_in(*items)
    return tanks


def main() -> None:
    """Launch the game."""
    tanks: Tanks = init_tanks()
    printer: Screen = Screen(tanks)
    commander: CommandHandler = CommandHandler(tanks)

    while True:
        commands: Commands = printer.display()
        commander.ask(commands)
        if tanks[-1].is_full:
            break

    print("You won !")


if __name__ == "__main__":
    main()
