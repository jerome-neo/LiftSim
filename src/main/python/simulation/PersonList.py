from src.main.python.simulation.LiftRandoms import LiftRandoms
from src.main.python.simulation.Person import Person


class PersonList:
    """A class representing a custom list of Person objects that have been pre-generated outside the simulation."""
    def __init__(self, duration_of_simulation, limit=300):
        """
        Initialize the list of Person objects taking into account the intended simulation duration and limit.

        Args:
            duration_of_simulation (int): duration to simulate.
            limit (int): maximum cap on the number of Person objects that can be generated.
        """
        self.list = []
        time = 0
        person_id = 1
        next_arrival_time = LiftRandoms().next_arrival_time(time)
        for i in range(duration_of_simulation):
            if person_id > limit:
                # we set a cap on the number of people we want to generate
                # this takes precedence over the duration_of_simulation
                break
            time += (next_arrival_time - time)  # update the 'clock'
            person = Person(person_id, next_arrival_time)
            self.list.append(person)
            # update the variables for next iteration
            person_id += 1
            next_arrival_time = LiftRandoms().next_arrival_time(time)

    def __str__(self):
        """
        Return a string representation of the PersonList.

        Returns:
            str: A string representation of the PersonList.
        """
        return str(list(map(lambda x: str(x), self.list)))

    def __len__(self):
        """Returns the length of the list."""
        return len(self.list)

    def get_person_list(self) -> list:
        """Returns the list."""
        return self.list

    def get_earliest_arrival_time(self) -> float:
        """Returns the earliest arrival time among the Persons in the PersonList"""
        for person in self.list:
            if not person.has_completed_trip():
                print(f'{person} arriving at floor {person.get_curr_floor()}, '
                      f'going to floor {person.get_dest_floor()} has not completed trip')
                return person.get_arrival_time()

    def get(self, index) -> Person:
        """Returns the Person at the specified index"""
        return self.list[index]
