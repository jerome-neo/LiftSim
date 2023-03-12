import random
import simpy
import numpy as np


MAX_CAPACITY = 8
MAX_WEIGHT = 1600 # kilograms
SPEED = (0.5, 0.6)


class Elevator(object):
    """
    Class representing an elevator in a building.

    Attributes:
        env (simpy.Environment): The simulation environment.
        index (int): The index of the elevator.
        floors (list): The collection of floors in the building.
        direction (str): The direction of travel for the elevator.
        max_persons (int): The maximum number of passengers the elevator can hold.
        max_weight (int): The maximum weight the elevator can hold.
        curr_floor (int): The current floor the elevator is on.
        speed (tuple): The speed of the elevator in meters per second.
        is_working_status (bool): The status of the elevator, busy or idle.
        passengers (list): The list of passengers in the elevator.
        path (list): The path the elevator will take to its next destination.

    Methods:
        __str__(): Returns a string representation of the elevator.
        get_direction(): Returns the direction of travel for the elevator.
        get_current_floor(): Returns the current floor the elevator is on.
        add_passengers(list_of_person): Adds a list of passengers to the elevator.
        enter_elevator(list_of_person): Simulates passengers entering the elevator.
        leave_elevator(): Simulates passengers leaving the elevator.
        is_busy(): Returns whether the elevator is busy or idle.
        set_busy(): Sets the elevator's status to busy.
        set_idle(): Sets the elevator's status to idle.
        travel(end): Simulates the elevator traveling to a floor.
        add_path(floor_level): Adds a floor to the path the elevator will take.
        get_path(): Returns the path the elevator will take.
        has_path(): Returns whether the elevator has a path to follow.

    """
    def __init__(self, env, index, collection_floors, curr_floor, direction):
        """
        Initializes an Elevator object with the specified parameters.

        Args:
            env (simpy.Environment): The simulation environment.
            index (int): The index of the elevator.
            collection_floors (list): The collection of floors in the building.
            curr_floor (int): The current floor the elevator is on.
            direction (str): The direction of travel for the elevator.

        """
        self.env = env
        self.index = index
        self.floors = collection_floors
        self.direction = direction
        self.max_persons = MAX_CAPACITY  # not implemented
        self.max_weight = MAX_WEIGHT  # not implemented
        self.curr_floor = curr_floor
        self.speed = SPEED  # metres per second
        self.is_working_status = False
        self.passengers = []
        self.path = []  # empty heap
        self.resource = simpy.Resource(env,1)

    def __str__(self):
        """Returns a string representation of the Elevator object."""
        return f"elevator {self.index} dedicated to {self.direction} calls is at " \
               f"{self.curr_floor} with {len(self.passengers)} person(s)"


    def get_direction(self) -> str:
        """Returns the direction of travel for the Elevator object."""
        return self.direction

    def get_current_floor(self) -> int:
        """Returns the current floor the Elevator object is on."""
        return self.curr_floor

    def add_passengers(self, person) -> None:
        """Adds a passenger to the Elevator object."""
        self.passengers.append(person)

    def enter_elevator(self, list_of_person) -> None:
        """Simulates passengers entering the Elevator object.

        Args:
            list_of_person (list): The list of passengers entering the elevator.

        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the passengers to enter

        """
        for person in list_of_person:
            self.add_passengers(person)
            floor_level = person.get_dest_floor()
            # Add items to the heap (priority, value)
            self.path.append(floor_level)
            print(f"{person} has entered {self}")
        self.path.sort()
        yield self.env.timeout(random.randint(2, 4))

    def leave_elevator(self) -> None:
        """
        Simulate passengers leaving the elevator.

        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the passengers to leave

        """
        to_remove = []
        for person in self.passengers:
            if person.has_reached_destination(self):
                person.complete_trip()
                to_remove.append(person)
                print(f"{person} has left {self}")
        for person in to_remove:
            self.passengers.remove(person)
        yield self.env.timeout(random.randint(2, 4))

    def is_busy(self) -> bool:
        """
        Check if the elevator is currently busy.

        Returns:
            bool: True if the elevator is currently busy, False otherwise

        """
        return self.is_working_status

    def set_busy(self) -> None:
        """Set the elevator to be busy."""
        self.is_working_status = True

    def set_idle(self) -> None:
        """Set the elevator to be idle."""
        self.is_working_status = False

    def travel(self, end) -> None:
        """
        Simulate the elevator traveling to a new floor.

        Args:
            end (int): the destination floor of the elevator

        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the elevator to travel to the
                destination floor

        """
        self.curr_floor = end

        with self.resource.request() as req:
            yield req
            yield self.env.timeout(abs(end - self.curr_floor) * 3)


    def add_path(self, floor_level) -> None:
        """
        Add a floor to the elevator's path.

        Args:
            floor_level (int): the floor to add to the elevator's path

        """
        self.path.append(floor_level)
        self.path = np.unique(self.path).tolist()
        self.path.sort()
        print(f"Path of elevator {self.index} going {self.direction}: {self.path}")

    def get_path(self) -> list:
        """
        Get the elevator's path.

        Returns:
            list: a list of floors the elevator will stop at in order

        """
        return self.path

    def has_path(self) -> bool:
        """
        Check if the elevator has a path.

        Returns:
            bool: True if the elevator has a path, False otherwise

        """
        return len(self.path) != 0
    
    
    def activate(self) -> None:
        """Activates elevator such that it immediately moves when a call is placed"""
        while self.has_path():
            print(f"Current path for elevator {self.index} going {self.direction}: {self.get_path()}")
            if self.get_direction() == "UP":
                next_floor = self.get_path()[::-1].pop()  # remove from the front
                yield self.env.process(self.travel(next_floor))
                floor = self.floors[next_floor - 1]
                if self.get_current_floor() != len(self.floors): #if elevator is currently on top-most level
                    yield self.env.process(self.enter_elevator(floor.remove_all_persons_going_up()))
                    floor.uncall_up()
                else:
                    yield self.env.process(self.travel(1))
            else:
                next_floor = self.get_path().pop()
                yield self.env.process(self.travel(next_floor))
                floor = self.floors[next_floor - 1]
                if self.get_current_floor() != 1:
                    yield self.env.process(self.enter_elevator(floor.remove_all_persons_going_down()))
                    floor.uncall_down()
                else:
                    yield self.env.process(self.travel(1))
            # take out passengers if any
            yield self.env.process(self.leave_elevator())


