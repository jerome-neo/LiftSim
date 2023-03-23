import random
import LiftRandoms

class Person(object):
    """A person in the building.

    Attributes:
        id (int): The unique identifier of the person.
        env (simpy.Environment): The simulation environment.
        curr_floor (int): The floor where the person is currently located.
        destination_floor (int): The floor where the person wants to go.
        arrival_time (float): The time when the person arrives in the building.
        end_time (float): The time when the person completes their trip.
        has_reached_floor (bool): Whether the person has reached their destination floor.

    """
    def __init__(self, env, index, building):
        """Initializes a new Person object.

        Args:
            env (simpy.Environment): The simulation environment.
            index (int): The unique identifier of the person.
            building (Building): The building where the person is located.

        """
        self.id = index
        self.env = env
        self.arrival_time = env.now

        random_variable_generator=LiftRandoms.LiftRandoms()
        self.curr_floor,self.destination_floor=random_variable_generator.generate_source_dest(self.arrival_time)
        
        self.end_time = None
        self.has_reached_floor = False
        print(f"Source: {self.curr_floor}, Dest: {self.destination_floor}")
        print(f"Arrival time: {self.arrival_time}")

    def __str__(self):
        """Returns a string representation of the Person object."""
        return f"Person {self.id} starting at {self.curr_floor} and going to {self.destination_floor}:"

    def calls_elevator(self) -> None:
        """
        Simulates a person calling an elevator.

        This method waits for one unit of time to simulate the time taken for a person to call an elevator.
        """
        yield self.env.timeout(1)

    def has_reached_destination(self, elevator) -> bool:
        """
        Checks if the person has reached their destination floor.

        Args:
            elevator (Elevator): The elevator that the person is in.

        Returns:
            bool: True if the person has reached their destination floor, False otherwise.

        """
        return elevator.get_current_floor() == self.destination_floor

    def complete_trip(self) -> None:
        """
        Marks the person's trip as complete.

        This method updates the end_time and has_reached_floor attributes to indicate that the person
        has completed their trip.

        """
        self.end_time = self.env.now
        self.has_reached_floor = True

    def has_completed_trip(self) -> bool:
        """
        Checks if the person has completed their trip.

        Returns:
            bool: True if the person has completed their trip, False otherwise.

        """
        return self.has_reached_floor

    def get_wait_time(self) -> float:
        """
        Returns the time taken for the person to complete their trip.

        Returns:
            float: The time taken for the person to complete their trip.

        """
        time_taken_to_complete = self.end_time - self.arrival_time
        return time_taken_to_complete

    def get_curr_floor(self) -> int:
        """
        Returns the current floor where the person is located.

        Returns:
            int: The current floor where the person is located.

        """
        return self.curr_floor

    def get_dest_floor(self) -> int:
        """
        Returns the destination floor where the person wants to go.

        Returns:
            int: The destination floor where the person wants to go.

        """
        return self.destination_floor

    def get_direction(self) -> int:
        """
        Returns the direction that the person wants to go.

        Returns:
            int: -1 if the person wants to go down, 1 if the person wants to go up.

        """
        return -1 if self.curr_floor > self.destination_floor else 1

