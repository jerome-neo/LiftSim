from typing import List

from .Floor import Floor


class GroundFloor(Floor):
    """A class representing the ground floor of a building, which is a subclass of the Floor class."""
    def __init__(self, env, index: int):
        """
        Initialize the ground floor with the given index.

        Args:
            env (simpy.Environment): The simulation environment.
            index (int): The index of the ground floor.

        """
        super().__init__(env, index)
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
        if not self.has_call_up() or self.going_up_persons[0].get_arrival_time() > self.env.now:
            return pointer
        else:
            n = len(self.going_up_persons)
            count = 0
            for i in range(n):
                if self.going_up_persons[i].get_arrival_time() > self.env.now:
                    break
                count += 1
            pointer = self.going_up_persons[:count]
            self.going_up_persons = self.going_up_persons[count+1:]
            return pointer

    def sort(self) -> None:
        """Sorts the list of Persons in ascending arrival time."""
        self.going_up_persons.sort(key=lambda person: person.get_arrival_time())

    def update(self) -> None:
        """Important to call this method every step of the simulation to update call status of every floor."""
        # Floor will "check" if people have arrived by peeking at the simulation time
        # to compare with the person's arrival time.
        if len(self.going_up_persons) != 0 and self.going_up_persons[0].get_arrival_time() <= self.env.now:
            self.set_call_up()
