import Elevator


class ModernEGCS(object):
    """
    A system for controlling a group of elevators in a building.

    Attributes:
        env (simpy.Environment): The simulation environment.
        floors (list of Floor): The collection of floors in the building.
        elevators_up (list of Elevator): The collection of elevators that move up.
        elevators_down (list of Elevator): The collection of elevators that move down.
    """
    def __init__(self, env, collection_floors, num_elevators):
        """
        Initializes an ElevatorSystem.

        Args:
            env (simpy.Environment): The simulation environment.
            collection_floors (list of Floor): The collection of floors in the building.
            num_elevators (int): The number of elevators in the system.

        """
        self.env = env
        self.floors = collection_floors
        self.elevators = [Elevator.Elevator(env, i, self.floors, 1, "UP") for i in range(1, num_elevators + 1)]
        


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
                list_of_elevators = sorted(self.elevators_down, key=lambda x: x.get_current_floor(), reverse=True)
                chosen_index = 0
                elevator = list_of_elevators[chosen_index]
                while elevator.is_busy():
                    chosen_index += 1
                    elevator = list_of_elevators[chosen_index]
                elevator.set_busy()
                for floor in self.floors:
                    if floor.has_call_down() and (floor.get_floor_level() not in elevator.path):
                        elevator.add_path(floor.get_floor_level())
                break

    def handle_rising_call(self) -> None:
        """Handles a rising call from a person who wants to go up."""
        while True:
            if all(map(lambda x: x.is_busy(), self.elevators_up)):
                yield self.env.timeout(1)
            else:
                list_of_elevators = sorted(self.elevators_up, key=lambda x: x.get_current_floor(), reverse=False)
                chosen_index = 0
                elevator = list_of_elevators[chosen_index]
                while elevator.is_busy():
                    chosen_index += 1
                    elevator = list_of_elevators[chosen_index]
                elevator.set_busy()
                for floor in self.floors:
                    if floor.has_call_up() and (floor.get_floor_level() not in elevator.path):
                        elevator.add_path(floor.get_floor_level())
                break


    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path."""
        for elevator in self.elevators_down + self.elevators_up:
            if not elevator.has_path() and elevator.is_busy():
                elevator.set_idle()
