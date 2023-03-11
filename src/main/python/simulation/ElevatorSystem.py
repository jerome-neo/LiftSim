import Elevator


class ElevatorSystem(object):
    """
    A system for controlling a group of elevators in a building.

    Attributes:
        env (simpy.Environment): The simulation environment.
        floors (list of Floor): The collection of floors in the building.
        elevators_up (list of Elevator): The collection of elevators that move up.
        elevators_down (list of Elevator): The collection of elevators that move down.
    """
    def __init__(self, env, collection_floors, num_up, num_down):
        """
        Initializes an ElevatorSystem.

        Args:
            env (simpy.Environment): The simulation environment.
            collection_floors (list of Floor): The collection of floors in the building.
            num_up (int): The number of elevators that move up.
            num_down (int): The number of elevators that move down.

        """
        self.env = env
        self.floors = collection_floors
        self.elevators_up = [Elevator.Elevator(env, i, self.floors, 1, "UP") for i in range(1, num_up + 1)]
        self.elevators_down = [Elevator.Elevator(env, i, self.floors, 1, "DOWN") for i in range(1, num_down + 1)]
        for elevator in self.elevators_up:
            elevator.activate()
        for elevator in self.elevators_down:
            elevator.activate()

    def __str__(self):
        """
        Returns a string representation of the ElevatorSystem.

        Returns:
            str: A string representation of the ElevatorSystem.

        """
        return f"Elevator with {len(self.elevators_up)} up and {len(self.elevators_down)} down configuration."

    def handle_person(self, person) -> None:
        """
        Handles a person who wants to use the elevator system.

        Args:
            person (Person): The person who wants to use the elevator system.
        """
        # Put the person in the floor and call the lift
        call_direction = person.get_direction()
        curr_floor = self.floors[person.get_curr_floor() - 1]
        if call_direction < 0:
            curr_floor.add_person_going_down(person)
            curr_floor.set_call_down()
        else:
            curr_floor.add_person_going_up(person)
            curr_floor.set_call_up()

    def handle_landing_call(self) -> None:
        """Handles a landing call from a person who wants to go down."""
        while True:
            if all(map(lambda x: x.is_busy(), self.elevators_down)):
                yield self.env.timeout(1)
            else:
                elevator = max(self.elevators_down, key=lambda x: x.get_current_floor())
                elevator.set_busy()
                for floor in self.floors:
                    if floor.has_call_down():
                        elevator.add_path(floor.get_floor_level())
                break

    def handle_rising_call(self) -> None:
        """Handles a rising call from a person who wants to go up."""
        while True:
            if all(map(lambda x: x.is_busy(), self.elevators_up)):
                yield self.env.timeout(1)
            else:
                elevator = min(self.elevators_up, key=lambda x: x.get_current_floor())
                elevator.set_busy()
                for floor in self.floors:
                    if floor.has_call_up():
                        elevator.add_path(floor.get_floor_level())
                break

    def move(self) -> None:
        """Moves the elevators and handles passengers getting on and off."""
        for elevator in self.elevators_down + self.elevators_up:
            while elevator.has_path():
                if elevator.get_direction() == "UP":
                    next_floor = elevator.get_path()[::-1].pop()  # remove from the front
                    yield self.env.process(elevator.travel(next_floor))
                    floor = self.floors[next_floor - 1]
                    if elevator.get_current_floor() != len(self.floors): #if elevator is currently on top-most level
                        yield self.env.process(elevator.enter_elevator(floor.remove_all_persons_going_up()))
                        floor.uncall_up()
                    else:
                        yield self.env.process(elevator.travel(1))
                else:
                    next_floor = elevator.get_path().pop()
                    yield self.env.process(elevator.travel(next_floor))
                    floor = self.floors[next_floor - 1]
                    if elevator.get_current_floor() != 1:
                        yield self.env.process(elevator.enter_elevator(floor.remove_all_persons_going_down()))
                        floor.uncall_down()
                    else:
                        yield self.env.process(elevator.travel(1))
                # take out passengers if any
                yield self.env.process(elevator.leave_elevator())

    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path."""
        for elevator in self.elevators_down + self.elevators_up:
            if not elevator.has_path() and elevator.is_busy():
                elevator.set_idle()
