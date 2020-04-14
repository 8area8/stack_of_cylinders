"""Tank module."""

from typing import Optional, List, Dict

from tanks import Tank, Screen, CommandHandler
from tanks.config import MAX_TANKS, MAX_ITEMS

# Personal types

Tanks = List["Tank"]
Commands = Dict[int, str]


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
    controls: CommandHandler = CommandHandler(tanks)

    while True:
        commands: Commands = printer.display()
        controls.wait_for(commands)
        if tanks[-1].is_full:
            break

    print("You won !")


if __name__ == "__main__":
    main()
