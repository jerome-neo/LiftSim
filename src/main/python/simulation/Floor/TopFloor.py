from .Floor import Floor


class TopFloor(Floor):
    """ A class representing the top floor of a building."""

    def __init__(self, index: int):
        """
        Initialize the top floor with the given index.

        Args:
            index (int): The index of the Top floor.

        """
        super().__init__(index)
        self.going_down_persons = []

    def __str__(self):
        """
        Return a string representation of the top floor.

        Returns:
            str: A string representation of the top floor.

        """
        return f"Top floor has {len(self.going_down_persons)} person(s) going down. Button pressed? {self.call_down}"

    def add_person_going_down(self, person) -> None:
        """
        Add a person to the list of those waiting to go down from this floor.

        Args:
            person: The person to be added.

        Returns:
            None

        """
        self.going_down_persons.append(person)

    def remove_all_persons_going_down(self) -> list:
        """
        Remove all people waiting to go down from this floor and return them.

        Returns:
            A list containing all the people waiting to go down from this floor.

        """
        pointer = []
        n = len(self.going_down_persons)
        for i in range(n):
            pointer.append(self.going_down_persons.pop())
        return pointer
    

    def get_all_persons_going_down(self) -> list:
        """
        Returns the list of all persons who want to go down from the top floor
        Returns:
            List[Person]: A list of all persons who want to go down from the top floor.
        """
        return self.going_down_persons