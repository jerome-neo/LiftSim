import random
import simpy
from src.main.python.simulation.Floor import Floor

MAX_CAPACITY = 13
MAX_WEIGHT = 1600  # kilograms
SPEED = (0.5, 0.6)


class Elevator(object):
    """
    Class representing an elevator in a building.

    Attributes:
        env (simpy.Environment): The simulation environment.
        index (int): The index of the elevator.
        floors (list): The collection of floors in the building.
        num_floors (int): Number of floors it is connected to.
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
            total_num_elevators (int): The number of elevators present in the system.
            direction (str): The direction of travel for the elevator. If not specified, as in for ModernEGCS,
            it is initially set as "NIL".

        """
        self.env = env
        self.index = index
        self.floors = collection_floors
        self.num_floors = len(collection_floors)
        self.direction = direction  # Otis algo if direction exist else ModernEGCS algo
        self.max_persons = MAX_CAPACITY  # todo: not implemented
        self.max_weight = MAX_WEIGHT  # todo: not implemented
        self.curr_floor = curr_floor
        self.speed = SPEED  # metres per second
        self.is_working_status = False
        self.passengers = []
        self.path = []  # all assigned floors in the elevator's current path based on simulation
        self.car_calls = []  # all un-served car calls registered for the elevator
        self.hall_calls = [] # all un-served hall calls registered for the elevator
        self.resource = simpy.Resource(env,1)
        self.capacity = MAX_CAPACITY
        self.is_moving = False
        self.total_num_elevators = total_num_elevators
        self.num_active_calls = 0  # actual number of active calls that the elevator is serving
        if direction == "NIL":
            self.lift_algo = "ModernEGCS"
        else:
            self.lift_algo = "Otis"

    def __str__(self):
        """Returns a string representation of the Elevator object."""
        return f"Elevator {self.index} set {self.direction} " \
               f"has passengers: {list(map(lambda x: str(x), self.passengers))}"

    def to_dict(self) -> dict:
        """Converts elevator information into a dictionary."""
        floor = {floor + 1: 0 for floor in range(self.num_floors)}
        floor[self.get_current_floor()] = 1
        return {'elevator_type': -1 if self.direction == "DOWN" else 1 if self.direction == "UP" else 0,
                'floor': floor, 'num_passengers': self.get_num_passengers()}
    
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
    
    def get_num_passengers(self):
        """Returns number of passengers inside."""
        return len(self.passengers)
  
    def add_passengers(self, person) -> None:
        """Adds a passenger to the Elevator object."""
        print(f'{person} has entered elevator {self.direction} {self.index}')
        self.passengers.append(person)
    

    def elevator_door_open(self, t=3):
        """Simulates door opening."""
        yield self.env.timeout(t)

    def elevator_door_close(self, t=3):
        """Simulates door closing."""
        yield self.env.timeout(t)

    def enter_elevator(self, list_of_person):
        """Simulates passengers entering the Elevator object.
        Args:
            list_of_person (list): The list of passengers entering the elevator.
        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the passengers to enter
        """
        for person in list_of_person:
            if len(self.passengers) < MAX_CAPACITY:
                self.add_passengers(person)
                person.elevator_arrival_time = self.env.now
                curr_level = self.curr_floor
                floor_level = person.get_dest_floor()
                if floor_level not in self.car_calls:
                    self.add_car_call(floor_level)
                print(f"{person} has entered elevator at simulation time: {self.env.now}")
            else:
                # Put them back into the floor if the elevator is full
                if self.get_direction() == "DOWN":
                    self.floors[self.get_current_floor() - 1].add_person_going_down(person)
                elif self.get_direction() == "UP":
                    self.floors[self.get_current_floor() - 1].add_person_going_up(person)
        # re-arrange our path back to ordering
        self.path.sort()
        # if we have people being put back into the floor
        self.floors[self.get_current_floor() - 1].sort()
        self.floors[self.get_current_floor() - 1].sort()
        if len(list_of_person) > 0:
            yield self.env.process(self.elevator_door_open())
            yield self.env.timeout(random.randint(2, 5))
            yield self.env.process(self.elevator_door_close())
        else:
            yield self.env.timeout(0)

    def leave_elevator(self):
        """
        Simulate passengers leaving the elevator.
        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the passengers to leave
        """
        to_remove = []
        for person in self.passengers:
            if person.has_reached_destination(self):
                print(f'{person} has reached destination floor')
                person.complete_trip(self.env.now)
                to_remove.append(person)
                print(f"{person} has left elevator at simulation time: {self.env.now}")
        for person in to_remove:
            self.passengers.remove(person)
        if self.curr_floor in self.car_calls:
            self.car_calls.remove(self.curr_floor)
        if self.curr_floor in self.hall_calls:
            self.hall_calls.remove(self.curr_floor)
        self.num_active_calls-=1
        if len(to_remove) > 0:
            yield self.env.process(self.elevator_door_open())
            yield self.env.timeout(random.randint(2, 5))
            yield self.env.process(self.elevator_door_close())
        else:
            yield self.env.timeout(0)
            
    def has_more_than_optimum_calls(self) -> bool:
        """Checks if elevator's number of calls is more than total number of floors // total number of elevators.
        Used in ModernEGCS."""
        return len(self.path)>len(self.floors)//self.total_num_elevators

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
        print(f'{self.direction} Elevator {self.index} has been set busy')

    def set_idle(self, lift_algo="Otis") -> None:
        """Set the elevator to be idle."""
        self.is_working_status = False
        if lift_algo == "ModernEGCS":
            self.direction = "NIL"
        print(f'{self.direction} Elevator {self.index} has been set idle')

    def travel(self, end) -> None:
        """
        Simulate the elevator traveling to a new floor.
        Args:
            end (int): the destination floor of the elevator
        """
        print(f'{self} moved from {self.curr_floor} to {end}')
        self.curr_floor = end
    
    def add_car_call(self, floor_level) -> None:
        """Adds a car call to the list of unserved car calls.

        Args:
            floor_level(int): destination floor level
        """
        if floor_level not in self.car_calls:
            self.car_calls.append(floor_level)
            self.car_calls.sort()
        if floor_level > self.curr_floor:
            self.direction = "UP"
        elif floor_level < self.curr_floor:
            self.direction = "DOWN"
        self.add_path(floor_level)
    
    def add_hall_call(self, floor_level: int, direction: str) -> bool:
        """Adds a hall call to the list of unserved hall calls and returns boolean indicating whether the
        hall call  has been successfully added to the list of hall calls.

        Args:
            floor_level (int): the floor from which hall call is initiated
            direction (str): the call direction
        Returns:
            True if call is successfully added to self.hall_calls, False otherwise"""
        if self.direction != "NIL" and self.direction != direction:
            return False
        if self.direction == "NIL":
            self.direction = direction
        if floor_level not in self.hall_calls:
            self.hall_calls.append(floor_level)
            self.num_active_calls += 1
        self.add_path(floor_level)
        return True

    def add_path(self, floor_level: int) -> None:
        """
        Add a floor to the elevator's path.

        Args:
            floor_level (int): the floor to add to the elevator's path
        """
        if self.direction == "NIL" and len(self.path) == 1: #elevator is initially an idling elevator sent to busy floor
            self.path = [] #change course immediately if a call is assigned to elevator
        if floor_level not in self.path:
            self.path.append(floor_level)
        
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
        return len(self.path) > 0

    def move(self):
        """This moves the elevator in the direction of the next floor in their path."""
        if self.has_path():
            destination_floor = self.get_path()[0] if self.get_direction() == "UP" else self.get_path()[-1]
            displacement_direction = destination_floor - self.get_current_floor()  # final - initial = change
            move_direction = "UP" if displacement_direction > 0 else "DOWN"
            if move_direction == "UP" and self.get_current_floor() != self.num_floors:
                self.travel(self.get_current_floor() + 1)
            elif move_direction == "DOWN" and self.get_current_floor() != 1:
                self.travel(self.get_current_floor() - 1)
            yield self.env.timeout(random.randint(3, 4))
        else:
            yield self.env.timeout(0)
        displayed_path = self.path if self.get_direction() == "UP" else self.path[::-1]
        print(f"Elevator {self.index} set {self.direction} has path logged: {displayed_path}")

    def activate(self) -> None:
        """
        This activates the logic of the elevator at the floor, here are the important functions:
            (1) It makes sure to check if the floor it is at is where they are supposed to be.
            (2) Allows boarding and leaving of passengers.
            (3) Updates the floor call statuses. It can only un-call it.
            (4) Updates the acceptance of a floor call status. It can only un-accept it.
        Note:
            Setting of the call status is done by the Floor class update() method.
            It should be called in the Building class.
        """
        if not self.is_busy() and not self.has_path():
            yield self.env.timeout(0)
        elif not self.has_path():
            # return control
            self.set_idle(self.lift_algo)
            yield self.env.timeout(0)
        else:
            if (self.get_path()[0] != self.get_current_floor() and self.direction == "UP") or \
                (self.get_path()[-1] != self.get_current_floor() and self.direction == "DOWN") or \
                (self.get_path()[0] != self.get_current_floor() and self.direction == "NIL"):
                print(f"Elevator {self.index} set {self.direction} "
                      f"knows that current floor {self.curr_floor} NOT IN path")
                yield self.env.timeout(0)
            else:
                print(f"Elevator {self.index} set {self.direction} "
                      f"knows that current floor {self.curr_floor} IN path")
                
                # Assuming we people are gracious
                # i.e. we let people leave the elevator before boarding
                yield self.env.process(self.leave_elevator())
                floor = self.floors[self.get_current_floor()-1]

                if self.get_direction() == "UP":
                    self.path.pop(0)
                    if self.get_current_floor() < self.num_floors:  
                        yield self.env.process(self.enter_elevator(floor.remove_all_persons_going_up()))
                        # reset status
                        floor.uncall_up()
                        floor.unaccept_up_call()
                elif self.get_direction() == "DOWN":
                    self.path.pop(-1)
                    if self.get_current_floor() > 1:
                        yield self.env.process(self.enter_elevator(floor.remove_all_persons_going_down()))
                        # reset status
                        floor.uncall_down()
                        floor.unaccept_down_call()
                else:
                    self.path.pop(0)
    
    def get_current_floor_object(self) -> Floor:
        """
        Returns the object of the current floor where the elevator is at.

        Returns:
            Floor: floor object of current floor where the elevator is at
        """
        floor_index = self.get_current_floor()-1
        return self.floors[floor_index]

    def get_passenger_count(self) -> int:
        """
        Returns the number of passengers that are currently in the elevator.

        Returns:
            int: length of self.passengers
        """
        return len(self.passengers)

    def get_passenger_list(self) -> list:
        """
        Returns a list of passengers that are currently in the elevator.

        Returns:
            list: list of Person objects of people currently inside the elevator
        """
        return self.passengers
    
    def car_calls_left(self) -> int:
        """
        Returns the number of car calls left

        Returns:
            int: length of self.car_calls
        """
        return len(self.car_calls)
    
    def get_car_calls(self) -> list:
        """
        Returns a list of floor levels for remaining car calls
        
        Returns:
            list: self.car_calls
        """
        return self.car_calls
    
    def unset_direction(self) -> None:
        """Changes direction to NIL once a ModernEGCS elevator has no more calls"""
        self.direction = "NIL"
    
    def is_serving_car_call(self) -> bool:
        """Returns True if elevator's next destination in path is from a car call"""
        if self.direction == "UP":
            return self.get_path()[0] in self.car_calls
        else:
            return self.get_path()[-1] in self.car_calls
    
    def floor_fits_path(self, floor_level: int) -> bool:
        """Returns True if floor level inputted does not disrupt the elevator's current movement
        Args:
            floor_level (int): floor level being assessed"""
        if self.direction == "UP":
            return self.get_current_floor() <= floor_level
        elif self.direction == "DOWN":
            return self.get_current_floor() >= floor_level
        else:
            return True
