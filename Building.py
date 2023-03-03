import simpy
import random
from Floor import TopFloor, GroundFloor, SandwichFloor
import Person
import ElevatorSystem


class Building(object):
    def __init__(self, env, num_up, num_down, num_floors):
        self.env = env
        self.num_up = num_up
        self.num_down = num_down
        self.elevators = simpy.Resource(env, num_up + num_down)
        self.num_floors = num_floors
        self.floors = []
        self.elevator_group = None
        self.all_persons_spawned = []

    def get_num_floors(self):
        return self.num_floors

    def initialise(self):
        self.floors.append(GroundFloor(1))
        self.floors.extend([SandwichFloor(i) for i in range(2, self.num_floors)])
        self.floors.append(TopFloor(self.num_floors))
        self.elevator_group = ElevatorSystem.ElevatorSystem(self.env, self.floors, self.num_up, self.num_down)

    def simulate(self, arrival_rate=0.5):
        system = ElevatorSystem.ElevatorSystem(self.env, self.floors, self.num_up, self.num_down)
        index = 0
        while True:
            # Generate arrive time of a Wave
            inter_arrival_time = random.expovariate(arrival_rate)
            yield self.env.timeout(inter_arrival_time)
            # Generate a number of people for that Wave
            num_people = random.randint(1, 30 + 1)
            wave = [Person.Person(self.env, index + i, self) for i in range(num_people + 1)]
            index += num_people  # update numbering
            self.all_persons_spawned.extend(wave)  # for calculating their waiting time

            # Place person into their respective floor
            for person in wave:
                system.handle_person(person)
            yield self.env.process(system.handle_rising_call())
            yield self.env.process(system.handle_landing_call())
            yield self.env.process(system.move())
            system.update_status()

