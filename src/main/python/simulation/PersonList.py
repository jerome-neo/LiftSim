import pandas as pd
import simpy
from LiftRandoms import LiftRandoms
from Person import Person


class PersonList:
    """A class representing a custom list of Person objects that have been pre-generated outside the simulation."""
    def __init__(self, env, duration_of_simulation, limit=300):
        """
        Initialize the list of Person objects taking into account the intended simulation duration and limit.
        Args:
            env: simpy.Environment on which simulation is running
            duration_of_simulation (int): duration to simulate.
            limit (int): maximum cap on the number of Person objects that can be generated.
        """
        self.env = env
        self.list = []
        self.limit = limit
        self.duration_of_simulation = duration_of_simulation

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

    def initialise(self, mode='default', path_to_data="../../in/input.csv"):
        if mode == 'manual':
            df = pd.read_csv(path_to_data)
            person_id = 1
            for index, row in df.iterrows():
                curr = row['curr']
                dest = row['dest']
                time = row['time']
                person = Person(self.env, person_id, time)
                person.overwrite(curr, dest)
                self.list.append(person)
                person_id += 1
            self.list.sort(key=lambda x: x.get_arrival_time())
        else:
            time = 0
            person_id = 1
            next_arrival_time = LiftRandoms().next_arrival_time(time)
            for i in range(self.duration_of_simulation):
                if person_id > self.limit:
                    # we set a cap on the number of people we want to generate
                    # this takes precedence over the duration_of_simulation
                    break
                time += (next_arrival_time - time)  # update the 'clock'
                person = Person(self.env, person_id, next_arrival_time)
                self.list.append(person)
                # update the variables for next iteration
                person_id += 1
                next_arrival_time = LiftRandoms().next_arrival_time(time)

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