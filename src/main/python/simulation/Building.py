import simpy
import random
from Floor import TopFloor, GroundFloor, SandwichFloor
import Person
import ElevatorSystem
import LiftRandoms


class Building(object):
    """
    A class representing a building.

    Attributes:
        env (simpy.Environment): The simulation environment.
        num_up (int): The number of elevators going up.
        num_down (int): The number of elevators going down.
        elevators (simpy.Resource): The elevators in the building.
        num_floors (int): The number of floors in the building.
        floors (list): A list containing all floors in the building.
        elevator_group (ElevatorSystem.ElevatorSystem): An instance of the ElevatorSystem class that manages the
            elevators in the building.
        all_persons_spawned (list): A list containing all Person instances created and placed in the building.

    Methods:
        get_num_floors(): Returns the number of floors in the building.
        initialise(): Initialises the building by adding the floors and the elevator system.
        simulate(): Simulates the building operation by creating Person instances, placing them in their
            respective floors, and managing the elevators in the building.

    """
    def __init__(self, env, num_up, num_down, num_floors):
        """
        Args:
            env (simpy.Environment): The simulation environment.
            num_up (int): The number of elevators going up.
            num_down (int): The number of elevators going down.
            num_floors (int): The number of floors in the building.

        """
        self.env = env
        self.num_up = num_up
        self.num_down = num_down
        self.num_floors = num_floors
        self.floors = []
        self.elevator_group = None
        self.all_persons_spawned = []

    def get_num_floors(self) -> int:
        """Returns the number of floors in the building."""
        return self.num_floors

    def initialise(self) -> None:
        """Initialises the building by adding the floors and the elevator system."""
        self.floors.append(GroundFloor(1))
        self.floors.extend([SandwichFloor(i) for i in range(2, self.num_floors)])
        self.floors.append(TopFloor(self.num_floors))
        self.elevator_group = ElevatorSystem.ElevatorSystem(self.env, self.floors, self.num_up, self.num_down)


    def simulate(self) -> None:
        """
        Simulates the building operation by creating Person instances, placing them in their respective floors, and managing the elevators in the building.

        Args:
            -

        Yields:
                The arrival time of each wave of Person instances.

        """
        random_variable_generator = LiftRandoms.LiftRandoms()
        index = 0
        while True:
            # Generate arrive time of a Wave
            inter_arrival_time = random_variable_generator.next_arrival_time(self.env.now)
            yield self.env.timeout(inter_arrival_time)
    
            index += 1  # update numbering
            # Generate person
            person = Person.Person(self.env, index, self)
            
            self.all_persons_spawned.append(person)  # for calculating waiting time
            self.elevator_group.update_status()

            # Otis handling of persons
            self.elevator_group.handle_person(person) #handle each incoming person
            self.env.process(self.elevator_group.handle_rising_call())
            self.env.process(self.elevator_group.handle_landing_call())

            for elevator in self.elevator_group.elevators_up:
                self.env.process(elevator.activate())
            
            for elevator in self.elevator_group.elevators_down:
                self.env.process(elevator.activate())
            
            