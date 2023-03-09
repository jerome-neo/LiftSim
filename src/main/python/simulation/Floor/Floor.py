class Floor(object):
    """A class representing a floor in a building."""
    def __init__(self, index: int):
        """
        Initialize the floor with the given index.

        Args:
            index (int): The index of the floor.
        """
        self.floor_index = index
        self.call_up = False
        self.call_down = False

    def __str__(self):
        """
        Return a string representation of the floor.

        Returns:
            str: A string representation of the floor.
        """
        return f"Floor {self.floor_index}"

    def has_call_down(self) -> bool:
        """
        Return True if there is a call for the elevator going down on this floor.

        Returns:
            bool: True if there is a call for the elevator going down on this floor, False otherwise.
        """
        return self.call_down

    def has_call_up(self) -> bool:
        """Set the call_up flag to True."""
        return self.call_up

    def set_call_up(self) -> bool:
        """Set the call_down flag to True."""
        self.call_up = True

    def set_call_down(self) -> None:
        """Set the call_up flag to False."""
        self.call_down = True

    def uncall_up(self) -> None:
        """Set the call_down flag to False."""
        self.call_up = False

    def uncall_down(self) -> None:
        """Set the call_down flag to False."""
        self.call_down = False

    def get_floor_level(self) -> int:
        """
        Return the index of the floor.

        Returns:
            int: The index of the floor.
        """
        return self.floor_index
