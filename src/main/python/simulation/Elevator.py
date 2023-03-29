import random
import simpy
import numpy as np
import Floor


MAX_CAPACITY = 13
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
    def __init__(self, env, index, collection_floors, curr_floor, total_num_elevators, direction="NIL"):
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
        self.direction = direction #if direction is inputted, we are running Otis algo, else we are running modern EGCS algo
        self.max_persons = MAX_CAPACITY  # not implemented
        self.max_weight = MAX_WEIGHT  # not implemented
        self.curr_floor = curr_floor
        self.speed = SPEED  # metres per second
        self.is_working_status = False
        self.passengers = []
        self.path = []  #all assigned floors in the elevator's current path
        self.car_calls = [] #all unserved car calls registered for the elevator
        self.resource = simpy.Resource(env,1)
        self.capacity = MAX_CAPACITY
        self.is_moving = False
        self.total_num_elevators = total_num_elevators

    def __str__(self):
        """Returns a string representation of the Elevator object."""
        return f"elevator {self.index} dedicated to {self.direction} calls is at " \
               f"{self.curr_floor} with {len(self.passengers)} person(s)"

    def get_index(self) -> int:
        """Returns the index of the elevator"""
        return self.index
    
    def get_direction(self) -> str:
        """Returns the direction of travel for the Elevator object."""
        return self.direction

    def get_capacity(self) -> int:
        """Returns the capacity of the Elevator object, i.e. maximum number of people inside the elevator"""
        return self.capacity

    def get_current_floor(self) -> int:
        """Returns the current floor the Elevator object is on."""
        return self.curr_floor

    def add_passengers(self, person) -> None:
        """Adds a passenger to the Elevator object."""
        self.passengers.append(person)
    
    def add_car_call(self,floor) -> None:
        """Adds a car call to the list of unserved car calls"""
        if floor not in self.car_calls:
            self.car_calls.append(floor)
            self.car_calls.sort()

    def enter_elevator(self, list_of_person) -> None:
        """Simulates passengers entering the Elevator object.

        Args:
            list_of_person (list): The list of passengers entering the elevator.

        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the passengers to enter

        """
        index=0
        while self.get_passenger_count()<self.get_capacity() and index<len(list_of_person)-1:
            person = list_of_person[index]
            self.add_passengers(person)
            person.succeeds_entering_elevator()
            floor_level = person.get_dest_floor()
            if floor_level not in self.path:
                self.add_path(floor_level)
                self.add_car_call(floor_level)
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
        for person in to_remove:
            self.passengers.remove(person)
        yield self.env.timeout(random.randint(2, 4))
    
    def has_more_than_optimum_calls(self) -> bool:
        """Checks if elevator's number of calls is more than total number of floors // total number of elevators. Used in ModernEGCS."""
        return len(self.path)>len(self.floors)//self.total_num_elevators

    def is_busy(self) -> bool:
        """
        Check if the elevator is currently busy.

        Returns:
            bool: True if the elevator is currently busy, False otherwise

        """
        return self.is_working_status
    
    def is_moving(self) -> bool:
        """
        Checks if the elevator is moving, i.e. in-between floors.

        Returns:
            bool: True if elevator is moving, False otherwise
        """
        return self.is_moving

    def set_busy(self) -> None:
        """Set the elevator to be busy."""
        self.is_working_status = True

    def set_idle(self) -> None:
        """Set the elevator to be idle."""
        self.is_working_status = False
    
    def set_moving(self)-> None:
        """Set the elevator as moving"""
        self.is_moving = True
    
    def set_stop_moving(self)-> None:
        """Set the elevator as not moving"""
        self.is_moving = False


    def travel(self, end) -> None:
        """
        Simulate the elevator traveling to a new floor.

        Args:
            end (int): the destination floor of the elevator

        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the elevator to travel to the
                destination floor

        """
        self.set_moving()
        self.curr_floor = end
        with self.resource.request() as req:
            yield req
            yield self.env.timeout(abs(end - self.curr_floor))
        self.path = self.path[1:]
        self.set_stop_moving()

    def add_path(self, floor_level,direction) -> None:
        """
        Add a floor from assigned hall call to the elevator's path.

        Args:
            floor_level (int): the floor to add to the elevator's path
            direction (str): the call direction

        """
        self.path.append(floor_level)
        if self.direction == direction:
            self.path = np.unique(self.path).tolist()
            self.path.sort()

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
    
    #might need to modify for modern EGCS
    def activate(self) -> None:
        """Activates elevator such that it immediately moves when a call is placed"""
        while self.has_path():
            if self.get_direction() == "UP":
                next_floor = self.get_path()[::-1].pop()  # remove from the front
                yield self.env.process(self.travel(next_floor))
                floor = self.floors[next_floor - 1]
                
                if self.get_current_floor() != len(self.floors): #if elevator is currently on top-most level
                    self.env.process(self.enter_elevator(floor.remove_all_persons_going_up()))
                self.env.process(self.leave_elevator()) # take out passengers if any
                floor.uncall_up()
                print(f"{self} at {self.env.now}")

            else:
                next_floor = self.get_path().pop()
                yield self.env.process(self.travel(next_floor))
                floor = self.floors[next_floor - 1]
                
                if self.get_current_floor() != 1:
                    self.env.process(self.enter_elevator(floor.remove_all_persons_going_down()))
                self.env.process(self.leave_elevator()) # take out passengers if any
                floor.uncall_down()
                print(f"{self} at {self.env.now}")
    
    def get_current_floor_object(self)->Floor:
        """
        Returns the object of the current floor where the elevator is at.

        Returns:
            Floor: floor object of current floor where the elevator is at
        """
        floor_index = self.get_current_floor()-1
        return self.floors[floor_index]

    def get_passenger_count(self)->int:
        """
        Returns the number of passengers that are currently in the elevator.

        Returns:
            int: length of self.passengers
        """
        return len(self.passengers)

    def get_passenger_list(self)->list:
        """
        Returns a list of passengers that are currently in the elevator.

        Returns:
            list: list of Person objects of people currently inside the elevator
        """
        return self.passengers
    
    def car_calls_left(self)-> int:
        """
        Returns the number of car calls left

        Returns:
            int: length of self.car_calls
        """
        return len(self.car_calls)
    
    def get_car_calls(self)-> list:
        """
        Returns a list of floor levels for remaining car calls
        
        Returns:
            list: self.car_calls
        """
        return self.car_calls

