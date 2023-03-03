import simpy
import random
import Floor
import Person
import Elevator


class Building(object):
    def __init__(self, env, num_elevators, num_floors):
        self.env = env
        self.num_elevators = num_elevators
        self.elevators = simpy.Resource(env, num_elevators)
        self.num_floors = num_floors
        self.floors = []
        self.elevator_group = []

    def initialise(self):
        self.floors.append(Floor.GroundFloor(1))
        self.floors.extend([Floor.SandwichFloor(i) for i in range(2, self.num_floors)])
        self.floors.append(Floor.TopFloor(self.num_floors))
        self.elevator_group.extend([Elevator(i, self.floors, 1) for i in range(1, self.num_elevators + 1)])

    def spawn(self, rate):
        inter_arrival_time = random.expovariate(rate)
        yield self.env.timeout(inter_arrival_time)
        return Person(self.env)

    def simulate(self, simulation_duration, arrival_rate=0.5):
        waiting_time = []

        while self.env.now() <= simulation_duration:
            new_person = self.spawn(arrival_rate)
            self.floors[new_person.get_curr_floor() - 1].append(new_person)
            if all(map(lambda x: x.is_servicing == False, self.elevator_group)):

            elif all(map(lambda x: x.is_servicing == False, self.elevator_group)):

            else:
                self.env.timeout(1)