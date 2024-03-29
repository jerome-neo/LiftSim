import simpy
from src.main.python.simulation.Floor import TopFloor, GroundFloor, SandwichFloor
from src.main.python.simulation.ElevatorSystem import ElevatorSystem
import src.main.python.simulation.ModernEGCS as ModernEGCS
import numpy as np


class Building(object):
    """
    A class representing a building.
    Attributes:
        env (simpy.Environment): The simulation environment.
        num_up (int): The number of elevators going up.
        num_down (int): The number of elevators going down.
        num_floors (int): The number of floors in the building.
        floors (list): A list containing all floors in the building.
        elevator_group (ElevatorSystem.ElevatorSystem): An instance of the ElevatorSystem class that manages the
            elevators in the building.
        all_persons_spawned (PersonList): A PersonList object containing all Person instances
        log: Log of every elevator state change
        arrival_rates_floors: This is for ModernECGS algo.
        elevator_algo: Elevator algorithm is either OTIS or ModernECGS.
    Methods:
        get_elevator_system(): Returns the object of the elevator system being implemented, which is either from the class ElevatorSystem (representing Otis) or ModernEGCS
        get_elevator_algo_type(): Returns in string the elevator system being implemented, which is either Otis or ModernEGCS
        get_num_floors(): Returns the number of floors in the building.
        get_all_persons(): Returns the PersonList object in the building.
        place_person_on_floor(): Distribute Person from PersonList into the floors.
        initialise(): Initialises the building by adding the floors and the elevator system.
        to_dict(): Returns a dictionary of logged information
        simulate(): Simulates the building operation by creating Person instances, placing them in their
            respective floors, and managing the elevators in the building.
        update_floor_arrival_rate(): Updates the value of arrival rate for a specified floor.
        get_sum_arrival_rates_floors(): Returns the sum of arrival rates across all floors.
        get_busiest_floor(): Returns floor level with the highest arrival rate.
    """
    def __init__(self, env, num_up, num_down, num_floors, persons_list):
        """
        Args:
            env (simpy.Environment): The simulation environment.
            num_up (int): The number of elevators going up.
            num_down (int): The number of elevators going down.
            num_floors (int): The number of floors in the building.
            persons_list (PersonList): The generated Persons used for simulation.
        """
        self.env = env
        self.num_up = num_up
        self.num_down = num_down
        self.num_floors = num_floors
        self.floors = []
        self.elevator_group = None
        self.all_persons_spawned = persons_list
        self.log = {}  # logs every step
        self.arrival_rates_floors = np.zeros(num_floors)
        self.elevator_algo = None
    
    def get_elevator_system(self):
        """Returns either ElevatorSystem or ModernEGCS object which is implemented as the building's elevator system"""
        return self.elevator_group
    
    def get_elevator_algo_type(self):
        """Returns in string the type of elevator algorithm implemented"""
        return self.elevator_algo
    
    def get_num_floors(self) -> int:
        """Returns the number of floors in the building."""
        return self.num_floors

    def get_all_persons(self) -> list:
        """Returns a list of Person objects that have been instantiated."""
        return self.all_persons_spawned

    def place_person_on_floor(self, person) -> None:
        """
        Places person into the simulation floor.
        Args:
            person (Person): The person who wants to use the elevator system.
        """
        # Put the person in the floor and call the lift
        call_direction = person.get_direction()
        curr_floor = self.floors[person.get_curr_floor() - 1]
        if call_direction == "DOWN":
            curr_floor.add_person_going_down(person)
        else:
            curr_floor.add_person_going_up(person)
    
    def initialise(self,elevator_algo) -> None:
        """Initialises all components that make up the building."""
        # Place floors into building
        self.floors.append(GroundFloor(self.env, 1))

        self.floors.extend([SandwichFloor(self.env, i) for i in range(2, self.num_floors)])
    
        self.floors.append(TopFloor(self.env, self.num_floors))
    
        # Place elevators into building
        if elevator_algo=="Otis":
            self.elevator_algo = "Otis"
            self.elevator_group = ElevatorSystem(self.env, self.floors, self.num_up, self.num_down)
        elif elevator_algo=="ModernEGCS":
            self.elevator_algo = "ModernEGCS"
            self.elevator_group = ModernEGCS.ModernEGCS(self.env, self, self.floors, num_elevators=self.num_up+self.num_down,w1=1,w2=1,w3=1)
            
        # Place persons into building
        for person in self.all_persons_spawned.get_person_list():
            self.place_person_on_floor(person)

    def to_dict(self) -> dict:
        """Returns a dictionary of the logged info."""
        return self.log

    def simulate(self):
        """
        Simulates the building operation by creating Person instances, placing them in their respective floors,
        and managing the elevators in the building.
        """

        while True:
            self.log.update(self.elevator_group.to_dict())
            print(f'Current simulation time: {self.env.now}')
            if self.env.now == 0 or self.elevator_group.is_all_idle():
                next_arrival_time = self.all_persons_spawned.get_earliest_arrival_time()
                if next_arrival_time >= self.env.now:
                    print(f"Fast-forwarding simulation time by {round(next_arrival_time - self.env.now)} unit(s)...")
                    yield self.env.timeout(round(next_arrival_time - self.env.now))
            # activate floor buttons if person 'arrived'
            for floor in self.floors:
                floor.update(self, self.elevator_group)

            if self.get_elevator_algo_type() == "Otis":
                self.elevator_group.allocate_rising_call()
                self.elevator_group.allocate_landing_call()

                for elevator in self.elevator_group.elevators_up:
                    yield self.env.process(elevator.activate())
                    yield self.env.process(elevator.move())

                for elevator in self.elevator_group.elevators_down:
                    yield self.env.process(elevator.activate())
                    yield self.env.process(elevator.move())

                self.elevator_group.update_status()
                yield self.env.timeout(1)
                print(self.elevator_group.print_system_status())
                print(f'\n')

            # ModernEGCS handling of persons
            elif self.get_elevator_algo_type() == "ModernEGCS":
                self.elevator_group.assign_calls()
                for elevator in self.elevator_group.elevators:
                    yield self.env.process(elevator.activate())
                    yield self.env.process(elevator.move())
                self.elevator_group.update_status()
                yield self.env.timeout(1)
                print(self.elevator_group.print_system_status())
                print(f'\n')

            else:
                print("Lift algorithm has not been configured yet")

    def update_floor_arrival_rate(self, floor_index, updated_rate):
        """Updates the value of arrival rate for a specified floor. Used in ModernEGCS calculations."""
        self.arrival_rates_floors[floor_index] = updated_rate
    
    def get_sum_arrival_rates_floors(self):
        """Returns the sum of arrival rates across all floors."""
        return np.sum(self.arrival_rates_floors)
    
    def get_busiest_floor(self):
        """Returns floor level with the highest arrival rate."""
        return np.argmax(self.arrival_rates_floors) + 1
