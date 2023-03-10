from .Floor import Floor


class SandwichFloor(Floor):
    """A class representing a floor of a building with people going up and down,
    which is a subclass of the Floor class."""
    def __init__(self, index: int):
        """
        Initialize the sandwich floor with the given index.

        Args:
            index (int): The index of the sandwich floor.

        """
        super().__init__(index)
        self.going_up_persons = []
        self.going_down_persons = []

    def __str__(self):
        """
        Return a string representation of the sandwich floor.

        Returns:
            str: A string representation of the sandwich floor.

        """
        return f"Floor {self.floor_index} has " \
               f"{len(self.going_up_persons)} person(s) going up and " \
               f"{len(self.going_down_persons)} person(s) going down. Buttons pressed? {self.call_up} {self.call_down}"

    def add_person_going_up(self, person) -> None:
        """
        Add a person who wants to go up from the sandwich floor.

        Args:
            person (Person): The person who wants to go up from the sandwich floor.

        """
        self.going_up_persons.append(person)

    def add_person_going_down(self, person) -> None:
        """
        Add a person who wants to go down from the sandwich floor.

            Args:
                person (Person): The person who wants to go down from the sandwich floor.

        """
        self.going_down_persons.append(person)

    def remove_all_persons_going_up(self) -> list:
        """
        Remove all persons who want to go up from the sandwich floor and return them as a list.

        Returns:
            List[Person]: A list of all persons who want to go up from the sandwich floor.

        """
        pointer = []
        n = len(self.going_up_persons)
        for i in range(n):
            pointer.append(self.going_up_persons.pop())
        return pointer

    def remove_all_persons_going_down(self) -> list:
        """
        Remove all persons who want to go down from the sandwich floor and return them as a list.

        Returns:
            List[Person]: A list of all persons who want to go down from the sandwich floor.

        """
        pointer = []
        n = len(self.going_down_persons)
        for i in range(n):
            pointer.append(self.going_down_persons.pop())
        return pointer
