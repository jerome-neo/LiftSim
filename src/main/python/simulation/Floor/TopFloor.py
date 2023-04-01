from Floor import Floor
from HallCall import HallCall
import simpy

class TopFloor(Floor):
    """ A class representing the top floor of a building."""

    def __init__(self, env: simpy.Environment, index: int):
        """
        Initialize the top floor with the given index.
        Args:
            env (simpy.Environment): The simulation environment.
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
            pointer = self.going_down_persons[:count]
            self.going_down_persons = self.going_down_persons[count + 1:]
            return pointer

    def sort(self) -> None:
        """Sorts the list of Persons in ascending arrival time."""
        self.going_down_persons.sort(key=lambda person: person.get_arrival_time())

    def update(self, building, elevator_system) -> None:
        """Important to call this method every step of the simulation to update call status of every floor."""
        # Floor will "check" if people have arrived by peeking at the simulation time
        # to compare with the person's arrival time.
        elevator_algo = elevator_system.get_algo_type()
        if len(self.going_down_persons) != 0 and self.going_down_persons[0].get_arrival_time() <= self.env.now:
            self.set_call_down()
            self.person_arrived(building)
            if elevator_algo == "ModernEGCS":
                print("Hall call registered")
                hall_call = HallCall(self.env,self.floor_index,-1)
                elevator_system.add_hall_call(hall_call)

    def get_all_persons_going_down(self) -> list:
        """
        Returns the list of all persons who want to go down from the top floor
        Returns:
            List[Person]: A list of all persons who want to go down from the top floor.
        """
        return self.going_down_persons