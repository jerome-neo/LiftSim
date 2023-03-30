import simpy

from src.main.python.simulation.LiftRandoms import LiftRandoms
from src.main.python.simulation.Person import Person


class PersonList:
    def __init__(self, duration_of_simulation, limit=300):
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
        return str(list(map(lambda x: str(x), self.list)))

    def __len__(self):
        return len(self.list)

    def get_person_list(self):
        return self.list

    def get_earliest_arrival_time(self):
        for person in self.list:
            if not person.has_completed_trip():
                print(f'{person} arriving at floor {person.get_curr_floor()}, '
                      f'going to floor {person.get_dest_floor()} has not completed trip')
                return person.get_arrival_time()

    def get(self, index):
        return self.list[index]

