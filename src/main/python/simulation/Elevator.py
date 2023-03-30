import random
import simpy
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
        self.num_floors = len(collection_floors)
        self.direction = direction
        self.max_persons = MAX_CAPACITY  # not implemented
        self.max_weight = MAX_WEIGHT  # not implemented
        self.curr_floor = curr_floor
        self.speed = SPEED  # metres per second
        self.is_working_status = False
        self.passengers = []
        self.path = []
        self.resource = simpy.Resource(env, 1)

    def __str__(self):
        """Returns a string representation of the Elevator object."""
        # return f"elevator {self.index} dedicated to {self.direction} calls is at " \
        #        f"{self.curr_floor} with {len(self.passengers)} person(s)"
        return f"{self.direction} Elevator {self.index} has passengers: {list(map(lambda x: str(x), self.passengers))}"

    def get_direction(self) -> str:
        """Returns the direction of travel for the Elevator object."""
        return self.direction

    def get_current_floor(self) -> int:
        """Returns the current floor the Elevator object is on."""
        return self.curr_floor

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
                floor_level = person.get_dest_floor()
                if floor_level not in self.path:
                    self.path.append(floor_level)
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
        if len(to_remove) > 0:
            yield self.env.process(self.elevator_door_open())
            yield self.env.timeout(random.randint(2, 5))
            yield self.env.process(self.elevator_door_close())
        else:
            yield self.env.timeout(0)

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

    def set_idle(self) -> None:
        """Set the elevator to be idle."""
        self.is_working_status = False
        print(f'{self.direction} Elevator {self.index} has been set idle')

    def travel(self, end):
        """
        Simulate the elevator traveling to a new floor.

        Args:
            end (int): the destination floor of the elevator

        Yields:
            simpy.events.Timeout: a timeout event representing the time it takes for the elevator to travel to the
                destination floor

        """
        print(f'{self} moved from {self.curr_floor} to {end}')
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
        # self.path = np.unique(self.path).tolist()
        self.path.sort()
        if not self.is_busy():
            self.set_busy()
        displayed_path = self.path if self.get_direction() == "UP" else self.path[::-1]
        print(f"{self.direction} elevator {self.index} path logged: {displayed_path}")

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
        # todo modify this to change the algorithm when it reaches top level
        if self.is_busy() and self.has_path():
            destination_floor = self.get_path()[0] if self.get_direction() == "UP" else self.get_path()[-1]
            displacement_direction = destination_floor - self.get_current_floor()  # final - initial = change
            move_direction = "UP" if displacement_direction > 0 else "DOWN"
            if move_direction == "UP" and self.get_current_floor() != self.num_floors:
                yield self.env.process(self.travel(self.get_current_floor() + 1))
            elif move_direction == "DOWN" and self.get_current_floor() != 1:
                yield self.env.process(self.travel(self.get_current_floor() - 1))
        else:
            yield self.env.timeout(0)

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
        if not self.is_busy():
            yield self.env.timeout(0)
        elif not self.has_path():
            # return control
            self.set_idle()
            yield self.env.timeout(0)
        else:
            if self.get_path()[0] != self.get_current_floor():
                print(f"{self.direction} Elevator {self.index} knows that current floor {self.curr_floor} NOT IN path")
                yield self.env.timeout(0)
            else:
                print(f"{self.direction} Elevator {self.index} knows that current floor {self.curr_floor} IN path")
                self.get_path().pop(0)

                # Assuming we people are gracious
                # i.e. we let people leave the elevator before boarding
                yield self.env.process(self.leave_elevator())
                floor = self.floors[self.get_current_floor()-1]

                if self.get_direction() == "UP":
                    if self.get_current_floor() < self.num_floors:  # if elevator is currently on top-most level
                        yield self.env.process(self.enter_elevator(floor.remove_all_persons_going_up()))
                        # reset status
                        floor.uncall_up()
                        floor.unaccept_up_call()
                elif self.get_direction() == "DOWN":
                    if self.get_current_floor() > 1:
                        yield self.env.process(self.enter_elevator(floor.remove_all_persons_going_down()))
                        # reset status
                        floor.uncall_down()
                        floor.unaccept_down_call()
