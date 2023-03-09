from typing import List

from .Floor import Floor


class GroundFloor(Floor):
    """A class representing the ground floor of a building, which is a subclass of the Floor class."""
    def __init__(self, index: int):
        """
        Initialize the ground floor with the given index.

        Args:
            index (int): The index of the ground floor.

        """
        super().__init__(index)
        self.going_up_persons = []

    def __str__(self):
        """
        Return a string representation of the ground floor.

        Returns:
            str: A string representation of the ground floor.

        """
        return f"Ground floor has {len(self.going_up_persons)} person(s) going up. Button pressed? {self.call_up}"

    def add_person_going_up(self, person) -> None:
        """
        Add a person who wants to go up from the ground floor.

        Args:
            person (Person): The person who wants to go up from the ground floor.

        """
        self.going_up_persons.append(person)

    def remove_all_persons_going_up(self) -> list:
        """
        Remove all persons who want to go up from the ground floor and return them as a list.

        Returns:
            List[Person]: A list of all persons who want to go up from the ground floor.

        """
        pointer = []
        n = len(self.going_up_persons)
        for i in range(n):
            pointer.append(self.going_up_persons.pop())
        return pointer
