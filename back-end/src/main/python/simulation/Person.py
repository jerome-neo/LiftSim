import src.main.python.simulation.LiftRandoms as LiftRandoms
from src.main.python.simulation.Elevator import Elevator


class Person(object):
    """A person in the building.
    Attributes:
        id (int): The unique identifier of the person.
        curr_floor (int): The floor where the person is currently located.
        destination_floor (int): The floor where the person wants to go.
        arrival_time (float): The time when the person arrives in the building.
        end_time (float): The time when the person completes their trip.
        has_reached_floor (bool): Whether the person has reached their destination floor.
    """
    def __init__(self, env, index, arrival_time):
        """Initializes a new Person object.
        Args:
            env (simpy.Environment): The simulation environment.
            index (int): The unique identifier of the person.
            arrival_time (float): Time person spawns.
        """
        self.id = index
        self.env = env
        self.arrival_time = arrival_time
        self.elevator_arrival_time = None  # time taken for the elevator to reach the person,
        # i.e. for the person's hall call to be answered
        self.end_time = None 
        self.curr_floor, self.destination_floor = LiftRandoms.LiftRandoms().generate_source_dest(self.arrival_time)
        self.has_reached_floor = False
        while self.curr_floor == self.destination_floor:
            self.curr_floor, self.destination_floor = LiftRandoms.LiftRandoms().generate_source_dest(self.arrival_time)

    def __str__(self):
        """Returns a string representation of the Person object."""
        return f"Person {self.id}"
    
    def reset(self, new_env):
        """Resets attributes so the same Person can be used in simulation using a different algorithm."""
        self.env = new_env
        self.elevator_arrival_time = None  # time taken for the elevator to reach the person,
        # i.e. for the person's hall call to be answered
        self.end_time = None 
        self.has_reached_floor = False

    def overwrite(self, curr_floor, destination_floor):
        """Overwrites automatic config of Person class."""
        self.curr_floor = curr_floor
        self.destination_floor = destination_floor
    
    def get_arrival_time(self):
        """Returns the person's arrival_time attribute."""
        return self.arrival_time

    def get_end_time(self):
        """Returns the end_time attribute."""
        return self.end_time

    def has_reached_destination(self, elevator) -> bool:
        """
        Checks if the person has reached their destination floor.

        Args:
            elevator (Elevator): The elevator that the person is in.

        Returns:
            bool: True if the person has reached their destination floor, False otherwise.

        """
        return elevator.get_current_floor() == self.destination_floor

    def complete_trip(self, time) -> None:
        """
        Marks the person's trip as complete.

        This method updates the end_time and has_reached_floor attributes to indicate that the person
        has completed their trip.

        """
        self.end_time = time
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

    def get_direction(self) -> str:
        """
        Returns the direction that the person wants to go.
        Returns:
            int: -1 if the person wants to go down, 1 if the person wants to go up.
        """
        return "DOWN" if self.curr_floor > self.destination_floor else "UP"

    def get_elevator_arrival_time(self) -> float:
        """
        Returns the person's assigned elevator's arrival time
        """
        return self.elevator_arrival_time
        
    def get_riding_time(self, elevator: Elevator) -> float:
        """
        Returns the estimated riding time of the person, which is time from the moment the person enters the assigned
        to the moment the person leaves the elevator, i.e. when the elevator has reached the person's destination.
        Used in ModernEGCS cost calculation.

        Args:
            elevator: The Elevator object it is assigned to during the calculation
        Returns:
            float: The length of time spent by the person in the elevator
        """
        if self.get_elevator_arrival_time() is None:
            elevator_arrival_to_now = 0
        else:
            elevator_arrival_to_now = self.env.now-self.get_elevator_arrival_time()
        assigned_elevator = elevator
        elevator_remaining_car_calls = assigned_elevator.get_car_calls()
        elevator_current_floor = assigned_elevator.get_current_floor()
        person_destination_floor = self.get_dest_floor()
        person_source_floor = self.get_curr_floor()
        to_wait_for_reaching_dest=0
        for floor in elevator_remaining_car_calls:
            if (floor > person_source_floor) and (floor < person_destination_floor):
                to_wait_for_reaching_dest += 1
            if floor >= person_destination_floor:
                break
        if assigned_elevator.get_direction() == "DOWN":
            to_wait_for_reaching_dest = len(elevator_remaining_car_calls) - to_wait_for_reaching_dest - 1
        
        estimated_remaining_travel_time = abs(person_destination_floor-elevator_current_floor) * 3.5\
            + 3.5 * to_wait_for_reaching_dest
        time_taken_to_ride = elevator_arrival_to_now + estimated_remaining_travel_time
        return time_taken_to_ride

    def get_elevator_waiting_time(self) -> float:
        """
        Returns the length of time spent waiting for the elevator to come and service the person's call.

        Returns:
            float: THe length of time spent waiting for the elevator by the person
        """
        time_taken_for_elevator_arrival = self.get_elevator_arrival_time() - self.get_arrival_time()
        return time_taken_for_elevator_arrival
