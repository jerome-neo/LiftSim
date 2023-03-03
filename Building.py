import simpy
import random
import Floor
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

    def initialise(self):
        self.floors.append(Floor.GroundFloor(1))
        self.floors.extend([Floor.SandwichFloor(i) for i in range(2, self.num_floors)])
        self.floors.append(Floor.TopFloor(self.num_floors))
        self.elevator_group = ElevatorSystem(self.floors, self.num_up, self.num_down)

    def spawn(self, rate):
        inter_arrival_time = random.expovariate(rate)
        yield self.env.timeout(inter_arrival_time)
        return Person(self.env)

    def simulate(self, simulation_duration, arrival_rate=0.5):
        waiting_time = []

        while self.env.now() <= simulation_duration:
            pass