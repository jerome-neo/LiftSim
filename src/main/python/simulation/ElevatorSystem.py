
import Elevator


class ElevatorSystem(object):
    """
    A system for controlling a group of elevators in a building.
    Uses traditional Otis elevators logic.
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
        self.num_floors = len(collection_floors)
        self.elevators_up = [Elevator.Elevator(env, i, self.floors, 1, num_up+num_down, direction="UP") for i in range(1, num_up + 1)]
        self.elevators_down = [Elevator.Elevator(env, i, self.floors, 1, num_up+num_down, direction="DOWN") for i in range(1, num_down + 1)]


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
        building = curr_floor.get_building()
        if call_direction < 0:
            curr_floor.add_person_going_down(person)
            curr_floor.person_arrived()
            curr_floor.set_call_down()
        else:
            curr_floor.add_person_going_up(person)
            curr_floor.person_arrived()
            curr_floor.set_call_up()
    


    def print_system_status(self) -> str:
        """Returns a string representation number of active elevators."""
        num_active_up = len(list(filter(lambda x: x.is_busy(), self.elevators_up)))
        num_active_down = len(list(filter(lambda x: x.is_busy(), self.elevators_down)))
        return f"Elevator system has {num_active_up} UP and {num_active_down} DOWN elevator(s) ACTIVE"

    def is_all_idle(self) -> bool:
        """Returns True if all the elevators are idle"""
        return all(map(lambda x: x.is_busy(), self.elevators_up)) \
            and all(map(lambda x: x.is_busy(), self.elevators_down))

    def allocate_landing_call(self) -> None:
        """Handles a landing call from a person who wants to go down."""
        if all(map(lambda x: x.is_call_down_accepted(), filter(lambda x: x.has_call_down(), self.floors))):
            return None
        if not all(map(lambda x: x.is_busy(), self.elevators_down)):
            list_of_elevators = sorted(self.elevators_down, key=lambda x: x.get_current_floor(), reverse=True)
            chosen_index = 0
            elevator = list_of_elevators[chosen_index]
            while elevator.is_busy():
                chosen_index += 1
                elevator = list_of_elevators[chosen_index]
            for floor in self.floors:
                if floor.is_call_down_accepted():
                    continue
                elif floor.has_call_down():
                    elevator.add_path(floor.get_floor_level())
                    floor.accept_down_call()

    def allocate_rising_call(self) -> None:
        """Handles a rising call from a person who wants to go up."""
        if all(map(lambda x: x.is_call_up_accepted(), filter(lambda x: x.has_call_up(), self.floors))):
            return None
        if not all(map(lambda x: x.is_busy(), self.elevators_up)):
            list_of_elevators = sorted(self.elevators_up, key=lambda x: x.get_current_floor(), reverse=False)
            chosen_index = 0
            elevator = list_of_elevators[chosen_index]
            while elevator.is_busy():
                chosen_index += 1
                elevator = list_of_elevators[chosen_index]
            elevator.set_busy()
            for floor in self.floors:
                if floor.is_call_up_accepted():
                    continue
                elif floor.has_call_up():
                    elevator.add_path(floor.get_floor_level())
                    floor.accept_up_call()

    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path."""
        for elevator in self.elevators_down + self.elevators_up:
            if not elevator.has_path() and elevator.is_busy():
                elevator.set_idle()