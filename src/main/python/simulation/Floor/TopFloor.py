from .Floor import Floor


class TopFloor(Floor):
    """ A class representing the top floor of a building."""

    def __init__(self, env, index: int):
        """
        Initialize the top floor with the given index.

        Args:
            index (int): The index of the Top floor.

        """
        super().__init__(env, index)
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
        Remove all persons who want to go down from the sandwich floor and return them as a list.

        Returns:
            List[Person]: A list of all persons who want to go down from the sandwich floor.

        """
        pointer = []
        if not self.has_call_down() or self.going_down_persons[0].get_arrival_time() > self.env.now:
            return pointer
        else:
            n = len(self.going_down_persons)
            count = 0
            for i in range(n):
                if self.going_down_persons[i].get_arrival_time() > self.env.now:
                    break
                count += 1
            if count > 0 and n > 0:
                for i in range(count):
                    pointer.append(self.going_down_persons.pop(i))
            return pointer

    def sort(self) -> None:
        self.going_down_persons.sort(key=lambda person: person.get_arrival_time())

    def update(self):
        # Floor will "check" if people have arrived by peeking at the simulation time
        # to compare with the person's arrival time.
        if len(self.going_down_persons) != 0 and self.going_down_persons[0].get_arrival_time() <= self.env.now:
            self.set_call_down()
