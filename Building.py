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
        self.floors.append(Floor.GroundFloor.GroundFloor(1))
        self.floors.extend([Floor.SandwichFloor.SandwichFloor(i) for i in range(2, self.num_floors)])
        self.floors.append(Floor.TopFloor.TopFloor(self.num_floors))
        self.elevator_group = ElevatorSystem.ElevatorSystem(self.floors, self.num_up, self.num_down)

    def simulate(self, simulation_duration, arrival_rate=0.5):
        waiting_time = []
        all_persons_spawned = []
        system = ElevatorSystem.ElevatorSystem(self.env, self.floors, self.num_up, self.num_down)

        while self.env.now() <= simulation_duration:
            # Generate arrive time of a Wave
            inter_arrival_time = random.expovariate(arrival_rate)
            yield self.env.timeout(inter_arrival_time)
            # Generate a number of people for that Wave
            num_people = random.randint(1, 30 + 1)
            wave = [Person() for i in range(num_people + 1)]
            all_persons_spawned.extend(wave)  # for calculating their waiting time

            # Place person into their respective floor
            for person in wave:
                system.handle_person(person)


            pass
