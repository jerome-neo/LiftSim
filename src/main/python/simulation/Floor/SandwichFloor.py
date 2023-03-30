from .Floor import Floor


class SandwichFloor(Floor):
    """A class representing a floor of a building with people going up and down,
    which is a subclass of the Floor class."""
    def __init__(self, env, index: int):
        """
        Initialize the sandwich floor with the given index.

        Args:
            index (int): The index of the sandwich floor.

        """
        super().__init__(env, index)
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
            if count > 0:
                for i in range(count):
                    pointer.append(self.going_up_persons.pop(i))
                return pointer
            return pointer

    def remove_all_persons_going_down(self) -> list:
        """
        Remove all persons who want to go down from the sandwich floor and return them as a list.

        Returns:
            List[Person]: A list of all persons who want to go down from the sandwich floor.

        """
        pointer = []
        if not self.has_call_up() or self.going_down_persons[0].get_arrival_time() > self.env.now:
            return pointer
        else:
            n = len(self.going_down_persons)
            count = 0
            for i in range(n):
                if self.going_down_persons[i].get_arrival_time() > self.env.now:
                    break
                count += 1
            if count > 0:
                for i in range(count):
                    pointer.append(self.going_down_persons.pop(i))
                return pointer

    def sort(self) -> None:
        self.going_up_persons.sort(key=lambda person: person.get_arrival_time())
        self.going_down_persons.sort(key=lambda person: person.get_arrival_time())

    def update(self):
        # Floor will "check" if people have arrived by peeking at the simulation time
        # to compare with the person's arrival time.
        if len(self.going_up_persons) != 0 and self.going_up_persons[0].get_arrival_time() <= self.env.now:
            self.set_call_up()
        if len(self.going_down_persons) != 0 and self.going_down_persons[0].get_arrival_time() <= self.env.now:
            self.set_call_down()

