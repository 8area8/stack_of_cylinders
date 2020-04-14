"""Tanks module.

Handle the tanks.
"""
from typing import Optional

from tanks.config import MAX_ITEMS


class Tank(list):
    """Tank class.

    Args:
        left (Tank, optional): the left linked tank.
        right (Tank, optional): the right linked tank.
    """

    def __init__(self, number: int, *args, **kwargs,) -> None:
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

    def add(self, item: int) -> None:
        """Parent append method.

        Args:
            item (int): the integer to append.
        """
        super().append(item)

    def append(self, _) -> None:
        """Raise AttributeError if called."""
        raise AttributeError("Do not use the 'append' method !")

    def move_to_(self, direction: str) -> bool:
        """Move the last item to the given direction.

        Remove the last item of the current tank. Give it the the linked tank.

        Args:
            direction (str): the wanted direction.

        Returns:
            bool: the result status.
        """
        inner_tank: Tank = getattr(self, direction, None)

        if inner_tank is not None and inner_tank.can_add(self[-1]):
            inner_tank.add(self.pop())
            return True

        print(f"Wrong direction: {direction} - {inner_tank} - {self[-1]}")
        return False

    def __str__(self) -> str:
        """Return the representation of Tank."""
        return f"Tank-{self.number}-{super().__str__()}"
